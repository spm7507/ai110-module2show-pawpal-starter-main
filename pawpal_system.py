"""PawPal+ core domain model.

Class skeleton generated from diagrams/uml.mmd. Attributes and method
signatures only — scheduling logic is intentionally left unimplemented.
Fill in the method bodies in small increments (see README workflow).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


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

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

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

    def describe(self) -> str:
        """Return a one-line summary, e.g. '08:00 — Morning walk (20 min)'."""
        return f"{self.start_time} — {self.task.describe()}"


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

    def sort_tasks(self) -> list[Task]:
        """Return tasks ordered by scheduling priority (most important first)."""
        return sorted(self.tasks, key=lambda task: task.priority_score(), reverse=True)

    def generate_schedule(self, start_time: str = "08:00") -> list[ScheduledItem]:
        """Select and order tasks into a daily plan within available time.

        Greedy fit: walk the tasks in priority order and place each one that
        still fits in the owner's remaining minutes, back-to-back from
        ``start_time``. Tasks that don't fit are skipped.
        """
        remaining = self.owner.get_available_minutes()
        current = _to_minutes(start_time)
        schedule: list[ScheduledItem] = []
        for task in self.sort_tasks():
            if task.duration_minutes <= remaining:
                schedule.append(ScheduledItem(_to_clock(current), task))
                current += task.duration_minutes
                remaining -= task.duration_minutes
        return schedule

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
