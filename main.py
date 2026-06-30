"""PawPal+ demo: build a small care plan and print today's schedule."""

from datetime import datetime

from pawpal_system import Owner, Pet, Priority, ScheduledItem, Scheduler, Task


def to_ampm(clock: str) -> str:
    """Convert a 'HH:MM' 24-hour string into 12-hour AM/PM, e.g. '08:55 AM'."""
    return datetime.strptime(clock, "%H:%M").strftime("%I:%M %p")


def main() -> None:
    # Create an owner and at least two pets.
    owner = Owner(name="Sam")
    owner.set_availability(120)  # 2 hours of care time today

    rex = Pet(name="Rex", species="dog", age=4)
    whiskers = Pet(name="Whiskers", species="cat", age=7)
    whiskers.add_care_need("daily medication")

    owner.add_pet(rex)
    owner.add_pet(whiskers)

    # Add tasks deliberately OUT OF TIME ORDER to prove the sorting works.
    scheduler = Scheduler(owner)
    scheduler.add_task(
        Task("Play time", duration_minutes=20, priority=Priority.LOW, pet=whiskers,
             time="17:00")
    )
    scheduler.add_task(
        Task("Morning walk", duration_minutes=30, priority=Priority.HIGH, pet=rex,
             time="08:00")
    )
    scheduler.add_task(
        Task("Feed breakfast", duration_minutes=15, priority=Priority.MEDIUM, pet=rex,
             time="07:30", completed=True)
    )
    scheduler.add_task(
        Task("Give medication", duration_minutes=10, priority=Priority.HIGH,
             pet=whiskers, time="07:00")
    )

    # 1) Sorting: tasks were added out of order — sort_tasks_by_time() fixes that.
    print("Tasks sorted by time")
    print("====================")
    for task in scheduler.sort_tasks_by_time():
        when = to_ampm(task.time) if task.time else "anytime"
        print(f"{when} — {task.describe()}")

    # 2) Filtering by pet name: just Rex's tasks.
    print("\nRex's tasks")
    print("===========")
    for task in scheduler.filter_tasks(pet_name="Rex"):
        print(f"- {task.describe()}")

    # 3) Filtering by completion status: what's still outstanding.
    print("\nOutstanding tasks (not yet done)")
    print("================================")
    for task in scheduler.filter_tasks(completed=False):
        print(f"- {task.describe()}")

    # 4) The schedule itself (completed tasks are skipped automatically).
    print("\nToday's Schedule")
    print("================")
    for item in scheduler.generate_schedule(start_time="08:00"):
        print(f"{to_ampm(item.start_time)} — {item.task.describe()}")

    # 5) Conflict detection: force two tasks into the SAME 08:00 slot.
    print("\nConflict Check")
    print("==============")
    clashing_schedule = [
        ScheduledItem("08:00", Task("Morning walk", duration_minutes=30, pet=rex)),
        ScheduledItem("08:00", Task("Give medication", duration_minutes=10, pet=whiskers)),
    ]
    warning = scheduler.conflict_warning(clashing_schedule)
    if warning:
        print(warning)
        print(scheduler.explain_conflicts(clashing_schedule))
    else:
        print("No conflicts — every scheduled task has the owner to itself.")


if __name__ == "__main__":
    main()
