"""Simple unit tests for the PawPal+ domain model."""

from pawpal_system import Owner, Pet, Priority, ScheduledItem, Scheduler, Task


def test_mark_complete_changes_status():
    """Task Completion: mark_complete() flips a task from not-done to done."""
    task = Task("Morning walk", duration_minutes=30)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Task Addition: adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Rex", species="dog", age=4)
    assert pet.task_count() == 0

    pet.add_task(Task("Morning walk", duration_minutes=30))

    assert pet.task_count() == 1


def _scheduler(*tasks: Task, minutes: int = 480) -> Scheduler:
    """Build a scheduler whose owner has ``minutes`` of availability."""
    owner = Owner(name="Sam")
    owner.set_availability(minutes)
    return Scheduler(owner, list(tasks))


def test_sort_by_time_orders_schedule_chronologically():
    """Sorting by time: items come back in start-time order regardless of input."""
    later = ScheduledItem("10:00", Task("Play", duration_minutes=20))
    earlier = ScheduledItem("08:00", Task("Walk", duration_minutes=30))

    ordered = Scheduler.sort_by_time([later, earlier])

    assert [item.start_time for item in ordered] == ["08:00", "10:00"]


def test_sort_tasks_by_time_orders_by_time_attribute():
    """Sorting tasks by time: timed tasks come first in time order, untimed last."""
    walk = Task("Walk", duration_minutes=30, time="09:00")
    meds = Task("Medication", duration_minutes=10, time="07:30")
    play = Task("Play", duration_minutes=20)  # no fixed time
    sched = _scheduler(walk, meds, play)

    ordered = sched.sort_tasks_by_time()

    assert [task.title for task in ordered] == ["Medication", "Walk", "Play"]


def test_filter_tasks_by_pet_and_status():
    """Filtering: filter_tasks narrows by pet and by completion status."""
    rex = Pet(name="Rex", species="dog", age=4)
    cat = Pet(name="Whiskers", species="cat", age=7)
    walk = Task("Walk", duration_minutes=30, pet=rex)
    done = Task("Feed", duration_minutes=10, pet=rex, completed=True)
    play = Task("Play", duration_minutes=20, pet=cat)
    sched = _scheduler(walk, done, play)

    assert sched.filter_tasks(pet=rex) == [walk, done]
    assert sched.filter_tasks(completed=False) == [walk, play]
    assert sched.filter_tasks(pet=rex, completed=False) == [walk]
    assert sched.filter_tasks(pet_name="rex") == [walk, done]  # case-insensitive
    assert sched.filter_tasks(pet_name="Whiskers", completed=False) == [play]


def test_completed_tasks_excluded_from_schedule_by_default():
    """Filtering: a completed task is not placed unless include_completed=True."""
    done = Task("Feed", duration_minutes=10, completed=True)
    sched = _scheduler(done)

    assert sched.generate_schedule() == []
    assert len(sched.generate_schedule(include_completed=True)) == 1


def test_recurring_task_is_placed_once_per_occurrence():
    """Recurring: a 2x/day task spaced 480 min apart yields two placements."""
    meds = Task(
        "Medication",
        duration_minutes=10,
        priority=Priority.HIGH,
        interval_minutes=480,
        occurrences=2,
    )
    sched = _scheduler(meds)

    schedule = sched.generate_schedule(start_time="08:00")

    assert meds.is_recurring() is True
    assert [item.start_time for item in schedule] == ["08:00", "16:00"]


def test_next_occurrence_advances_date_by_frequency():
    """Recurrence: daily advances one day, weekly seven; copy is not completed."""
    daily = Task("Walk", duration_minutes=30, date="2026-06-29", recurrence="daily")
    weekly = Task("Bath", duration_minutes=45, date="2026-06-29", recurrence="weekly")

    next_daily = daily.next_occurrence()
    next_weekly = weekly.next_occurrence()

    assert next_daily.date == "2026-06-30"
    assert next_weekly.date == "2026-07-06"
    assert next_daily.completed is False


def test_next_occurrence_returns_none_for_one_off():
    """Recurrence: a non-recurring task produces no next occurrence."""
    one_off = Task("Vet visit", duration_minutes=60, recurrence=None)

    assert one_off.next_occurrence() is None


def test_complete_task_auto_queues_next_occurrence():
    """Recurrence: completing a daily task adds a fresh instance to the pool."""
    walk = Task("Walk", duration_minutes=30, date="2026-06-29", recurrence="daily")
    sched = _scheduler(walk)

    upcoming = sched.complete_task(walk)

    assert walk.completed is True
    assert upcoming in sched.tasks
    assert upcoming.completed is False
    assert upcoming.date == "2026-06-30"


def test_complete_task_one_off_adds_nothing():
    """Recurrence: completing a one-off task leaves the pool size unchanged."""
    vet = Task("Vet visit", duration_minutes=60)
    sched = _scheduler(vet)

    assert sched.complete_task(vet) is None
    assert sched.tasks == [vet]


def test_detect_conflicts_flags_overlapping_items():
    """Conflict detection: overlapping ranges are reported, back-to-back are not."""
    walk = ScheduledItem("08:00", Task("Walk", duration_minutes=30))
    overlap = ScheduledItem("08:15", Task("Vet", duration_minutes=30))
    adjacent = ScheduledItem("08:45", Task("Feed", duration_minutes=10))
    sched = _scheduler()

    conflicts = sched.detect_conflicts([walk, overlap, adjacent])

    assert conflicts == [(walk, overlap)]


def test_find_conflicts_classifies_same_pet_vs_different_pets():
    """Conflict scope: overlaps are tagged same_pet vs. cross-pet correctly."""
    rex = Pet(name="Rex", species="dog", age=4)
    cat = Pet(name="Whiskers", species="cat", age=7)
    rex_walk = ScheduledItem("08:00", Task("Walk", duration_minutes=30, pet=rex))
    rex_feed = ScheduledItem("08:15", Task("Feed", duration_minutes=10, pet=rex))
    cat_meds = ScheduledItem("08:28", Task("Meds", duration_minutes=10, pet=cat))
    sched = _scheduler()

    conflicts = sched.find_conflicts([rex_walk, rex_feed, cat_meds])

    # Rex's walk (08:00–08:30) overlaps both Rex's feed and the cat's meds.
    same = [c for c in conflicts if c.same_pet]
    cross = [c for c in conflicts if not c.same_pet]
    assert len(same) == 1 and same[0].first.task.title == "Walk"
    assert len(cross) == 1 and cross[0].second.task.title == "Meds"


def test_explain_conflicts_reports_none_when_clear():
    """Conflict report: back-to-back tasks produce a clean, no-conflict message."""
    sched = _scheduler()
    a = ScheduledItem("08:00", Task("Walk", duration_minutes=30))
    b = ScheduledItem("08:30", Task("Feed", duration_minutes=10))

    assert "No conflicts" in sched.explain_conflicts([a, b])


def test_conflict_warning_returns_message_or_none():
    """Lightweight check: warns on overlap, returns None when the plan is clear."""
    sched = _scheduler()
    walk = ScheduledItem("08:00", Task("Walk", duration_minutes=30))
    overlap = ScheduledItem("08:15", Task("Vet", duration_minutes=30))
    clear = ScheduledItem("08:30", Task("Feed", duration_minutes=10))

    assert sched.conflict_warning([walk, overlap]).startswith("⚠️")
    assert sched.conflict_warning([walk, clear]) is None


def test_conflict_warning_does_not_crash_on_bad_time():
    """Lightweight check: a malformed time yields a warning, not an exception."""
    sched = _scheduler()
    good = ScheduledItem("08:00", Task("Walk", duration_minutes=30))
    bad = ScheduledItem("not-a-time", Task("Vet", duration_minutes=30))

    message = sched.conflict_warning([good, bad])

    assert message is not None and "invalid time" in message
