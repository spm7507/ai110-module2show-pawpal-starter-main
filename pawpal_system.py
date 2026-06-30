"""PawPal+ core domain model.

Class skeleton generated from diagrams/uml.mmd. Attributes and method
signatures only — scheduling logic is intentionally left unimplemented.
Fill in the method bodies in small increments (see README workflow).
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from enum import IntEnum

# Cross-day recurrence frequencies and how many days each advances.
_RECURRENCE_STEPS = {"daily": 1, "weekly": 7}


class Priority(IntEnum):
    """Task priority. IntEnum so values double as a sort/score key."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


def _to_minutes(clock: str) -> int:
    """Convert a 'HH:MM' string into minutes since midnight."""
    hours, minutes = clock.split(":")
    return int(hours) * 60 + int(minutes)


def _to_clock(total_minutes: int) -> str:
    """Convert minutes since midnight into a 'HH:MM' string (wraps at 24h)."""
    total_minutes %= 24 * 60
    return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"


@dataclass
class Pet:
    """A pet that care tasks are planned for."""

    name: str
    species: str
    age: int
    special_care_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_care_need(self, need: str) -> None:
        """Record a special care need (e.g. 'daily medication')."""
        need = need.strip()
        if need and need not in self.special_care_needs:
            self.special_care_needs.append(need)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        if task not in self.tasks:
            self.tasks.append(task)

    def task_count(self) -> int:
        """Return how many tasks are attached to this pet."""
        return len(self.tasks)

    def describe(self) -> str:
        """Return a human-readable summary of the pet."""
        summary = f"{self.name} ({self.species}, {self.age}y)"
        if self.special_care_needs:
            summary += f" — needs: {', '.join(self.special_care_needs)}"
        return summary


@dataclass
class Owner:
    """The pet owner: their preferences and time available for care."""

    name: str
    preferences: dict[str, str] = field(default_factory=dict)
    available_minutes: int = 0
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to this owner."""
        if pet not in self.pets:
            self.pets.append(pet)

    def set_availability(self, minutes: int) -> None:
        """Set how many minutes the owner has for pet care today."""
        if minutes < 0:
            raise ValueError("available minutes cannot be negative")
        self.available_minutes = minutes

    def get_available_minutes(self) -> int:
        """Return the owner's available care time in minutes."""
        return self.available_minutes


@dataclass
class Task:
    """A single pet care activity to be scheduled."""

    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    description: str = ""
    pet: Pet | None = None
    completed: bool = False
    # Optional preferred time of day as "HH:MM"; None means "no fixed time".
    time: str | None = None
    # Optional calendar date this occurrence falls on, as "YYYY-MM-DD".
    date: str | None = None
    # Cross-day recurrence: "daily" or "weekly" (None = one-off). On completion
    # the next occurrence is generated (see ``next_occurrence``).
    recurrence: str | None = None
    # In-day recurrence: repeat ``occurrences`` times today, each spaced
    # ``interval_minutes`` apart (e.g. medication every 8h => interval 480, 2x).
    interval_minutes: int = 0
    occurrences: int = 1

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Return True if this task should be placed more than once today."""
        return self.occurrences > 1 and self.interval_minutes > 0

    def next_occurrence(self) -> Task | None:
        """Build the next instance of a daily/weekly task, or None if one-off.

        Returns a fresh, not-completed copy carrying over every field (title,
        duration, priority, time, pet, recurrence, ...). If this task has a
        ``date``, it is advanced one day for "daily" or seven for "weekly";
        with no date set, the copy simply represents the next round.
        """
        step = _RECURRENCE_STEPS.get(self.recurrence)
        if step is None:
            return None
        next_date = self.date
        if self.date is not None:
            next_date = (date.fromisoformat(self.date) + timedelta(days=step)).isoformat()
        return replace(self, completed=False, date=next_date)

    def priority_score(self) -> int:
        """Return a numeric score used to rank this task.

        Higher is more important. Priority dominates; the duration acts as a
        small tie-breaker so shorter tasks of equal priority rank first.
        """
        return self.priority * 1000 - self.duration_minutes

    def describe(self) -> str:
        """Return a human-readable summary of the task."""
        summary = f"{self.title} ({self.duration_minutes} min) [priority: {self.priority.name.lower()}]"
        if self.pet is not None:
            summary += f" for {self.pet.name}"
        return summary


@dataclass
class ScheduledItem:
    """A task placed at a specific start time in the daily plan."""

    start_time: str  # "HH:MM"
    task: Task

    def start_minutes(self) -> int:
        """Return the start time as minutes since midnight."""
        return _to_minutes(self.start_time)

    def end_minutes(self) -> int:
        """Return the end time as minutes since midnight."""
        return self.start_minutes() + self.task.duration_minutes

    def end_time(self) -> str:
        """Return the 'HH:MM' time this item finishes."""
        return _to_clock(self.end_minutes())

    def overlaps(self, other: ScheduledItem) -> bool:
        """Return True if this item's time range overlaps ``other``'s.

        Ranges are half-open [start, end), so back-to-back items (one ending
        exactly when the next begins) do not count as a conflict.
        """
        return (
            self.start_minutes() < other.end_minutes()
            and other.start_minutes() < self.end_minutes()
        )

    def describe(self) -> str:
        """Return a one-line summary, e.g. '08:00 — Morning walk (20 min)'."""
        return f"{self.start_time} — {self.task.describe()}"


@dataclass
class Conflict:
    """Two scheduled items whose time ranges overlap."""

    first: ScheduledItem
    second: ScheduledItem

    @property
    def same_pet(self) -> bool:
        """True if both tasks belong to the same (non-None) pet."""
        pet_a = self.first.task.pet
        pet_b = self.second.task.pet
        return pet_a is not None and pet_a is pet_b

    def describe(self) -> str:
        """Return a human-readable summary noting the scope of the clash."""
        if self.same_pet:
            scope = f"same pet ({self.first.task.pet.name})"
        else:
            scope = "different pets"
        return (
            f"Conflict [{scope}]: '{self.first.task.title}' "
            f"({self.first.start_time}–{self.first.end_time()}) overlaps "
            f"'{self.second.task.title}' "
            f"({self.second.start_time}–{self.second.end_time()})"
        )


class Scheduler:
    """Manages tasks and builds a daily plan from the owner's constraints."""

    def __init__(self, owner: Owner, tasks: list[Task] | None = None) -> None:
        self.owner = owner
        self.tasks: list[Task] = tasks if tasks is not None else []

    def add_task(self, task: Task) -> None:
        """Add a task to the pool of candidate tasks."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the candidate pool."""
        if task in self.tasks:
            self.tasks.remove(task)

    def complete_task(self, task: Task) -> Task | None:
        """Mark ``task`` complete and auto-queue its next occurrence if it recurs.

        For a "daily" or "weekly" task this builds the next instance, adds it to
        the candidate pool (and to its pet, if any), and returns it. One-off
        tasks just get marked complete and return None.
        """
        task.mark_complete()
        upcoming = task.next_occurrence()
        if upcoming is not None:
            self.add_task(upcoming)
            if upcoming.pet is not None:
                upcoming.pet.add_task(upcoming)
        return upcoming

    def sort_tasks(self) -> list[Task]:
        """Return tasks ordered by scheduling priority (most important first)."""
        return sorted(self.tasks, key=lambda task: task.priority_score(), reverse=True)

    def filter_tasks(
        self,
        *,
        pet: Pet | None = None,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return candidate tasks filtered by pet, pet name, and/or status.

        Every argument defaults to ``None``, which leaves that dimension
        unfiltered. Pass ``completed=False`` for outstanding tasks only, a
        specific ``pet`` object, or a ``pet_name`` (case-insensitive) to get
        just that pet's tasks.
        """
        result = list(self.tasks)
        if pet is not None:
            result = [task for task in result if task.pet is pet]
        if pet_name is not None:
            key = pet_name.strip().casefold()
            result = [
                task
                for task in result
                if task.pet is not None and task.pet.name.casefold() == key
            ]
        if completed is not None:
            result = [task for task in result if task.completed is completed]
        return result

    @staticmethod
    def sort_by_time(schedule: list[ScheduledItem]) -> list[ScheduledItem]:
        """Return scheduled items ordered chronologically by start time."""
        return sorted(schedule, key=lambda item: item.start_minutes())

    def sort_tasks_by_time(self) -> list[Task]:
        """Return candidate tasks ordered by their preferred ``time`` attribute.

        Tasks with no fixed time (``time is None``) sort after timed ones, so a
        plan leads with the fixed-time tasks and trails with the flexible ones.
        """
        return sorted(
            self.tasks,
            key=lambda task: _to_minutes(task.time) if task.time else 24 * 60,
        )

    def generate_schedule(
        self, start_time: str = "08:00", include_completed: bool = False
    ) -> list[ScheduledItem]:
        """Select and order tasks into a daily plan within available time.

        Greedy fit: walk the tasks in priority order and place each one that
        still fits in the owner's remaining minutes, back-to-back from
        ``start_time``. Completed tasks are skipped unless ``include_completed``
        is set. A recurring task reserves time for all of its occurrences and is
        placed once per occurrence, spaced ``interval_minutes`` apart; later
        occurrences are pinned to that interval, so they may overlap other tasks
        (use :meth:`detect_conflicts` to surface those).
        """
        remaining = self.owner.get_available_minutes()
        current = _to_minutes(start_time)
        schedule: list[ScheduledItem] = []
        candidates = self.sort_tasks()
        if not include_completed:
            candidates = [task for task in candidates if not task.completed]
        for task in candidates:
            needed = task.duration_minutes * task.occurrences
            if needed <= remaining:
                for k in range(task.occurrences):
                    start = current + k * task.interval_minutes
                    schedule.append(ScheduledItem(_to_clock(start), task))
                current += task.duration_minutes
                remaining -= needed
        return schedule

    def find_conflicts(
        self, schedule: list[ScheduledItem] | None = None
    ) -> list[Conflict]:
        """Return every overlapping pair of scheduled items as ``Conflict``s.

        Defaults to the current generated schedule. Items are compared after
        sorting by start time; each overlapping pair is reported once. Use a
        conflict's ``same_pet`` flag to tell apart a clash within one pet's care
        (two of Rex's tasks at once) from a cross-pet clash (Rex and Whiskers
        needing the owner simultaneously).
        """
        if schedule is None:
            schedule = self.generate_schedule()
        ordered = self.sort_by_time(schedule)
        conflicts: list[Conflict] = []
        for i, earlier in enumerate(ordered):
            for later in ordered[i + 1 :]:
                if earlier.overlaps(later):
                    conflicts.append(Conflict(earlier, later))
        return conflicts

    def detect_conflicts(
        self, schedule: list[ScheduledItem] | None = None
    ) -> list[tuple[ScheduledItem, ScheduledItem]]:
        """Return overlapping pairs as ``(earlier, later)`` tuples.

        Thin wrapper over :meth:`find_conflicts` for callers that just want the
        raw item pairs without the same-pet/cross-pet classification.
        """
        return [(c.first, c.second) for c in self.find_conflicts(schedule)]

    def explain_conflicts(self, schedule: list[ScheduledItem] | None = None) -> str:
        """Return a human-readable report of all scheduling conflicts."""
        conflicts = self.find_conflicts(schedule)
        if not conflicts:
            return "No conflicts — every scheduled task has the owner to itself."
        lines = [f"Found {len(conflicts)} conflict(s):"]
        lines.extend(f"  {conflict.describe()}" for conflict in conflicts)
        return "\n".join(lines)

    def conflict_warning(self, schedule: list[ScheduledItem] | None = None) -> str | None:
        """Lightweight conflict check that returns a warning instead of raising.

        Returns a short one-line warning when overlaps are found — or when the
        schedule can't be evaluated (e.g. a task has a malformed time) — and
        ``None`` when the plan looks clear. Safe to call directly in UI code
        without wrapping it in try/except.
        """
        try:
            conflicts = self.find_conflicts(schedule)
        except (ValueError, AttributeError):
            return "⚠️ Couldn't check conflicts: some tasks have invalid time values."
        if not conflicts:
            return None
        same = sum(1 for conflict in conflicts if conflict.same_pet)
        cross = len(conflicts) - same
        scope = []
        if same:
            scope.append(f"{same} same-pet")
        if cross:
            scope.append(f"{cross} cross-pet")
        return (
            f"⚠️ {len(conflicts)} scheduling conflict(s) detected "
            f"({', '.join(scope)}) — consider freeing time or rescheduling."
        )

    def explain(self) -> str:
        """Explain why each task was chosen and when it was placed."""
        schedule = self.generate_schedule()
        placed = {item.task for item in schedule}
        budget = self.owner.get_available_minutes()
        used = sum(item.task.duration_minutes for item in schedule)

        lines = [
            f"Daily plan for {self.owner.name} "
            f"({used} of {budget} min used, {budget - used} min free):"
        ]
        if schedule:
            for item in schedule:
                lines.append(
                    f"  {item.describe()} — chosen as a "
                    f"{item.task.priority.name.lower()}-priority task that fit the time budget"
                )
        else:
            lines.append("  (nothing scheduled — no tasks fit the available time)")

        skipped = [task for task in self.sort_tasks() if task not in placed]
        for task in skipped:
            lines.append(
                f"  skipped: {task.describe()} — not enough remaining time"
            )
        return "\n".join(lines)
