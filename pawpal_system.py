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


@dataclass
class Pet:
    """A pet that care tasks are planned for."""

    name: str
    species: str
    age: int
    special_care_needs: list[str] = field(default_factory=list)

    def add_care_need(self, need: str) -> None:
        """Record a special care need (e.g. 'daily medication')."""
        raise NotImplementedError

    def describe(self) -> str:
        """Return a human-readable summary of the pet."""
        raise NotImplementedError


@dataclass
class Owner:
    """The pet owner: their preferences and time available for care."""

    name: str
    preferences: dict[str, str] = field(default_factory=dict)
    available_minutes: int = 0
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to this owner."""
        raise NotImplementedError

    def set_availability(self, minutes: int) -> None:
        """Set how many minutes the owner has for pet care today."""
        raise NotImplementedError

    def get_available_minutes(self) -> int:
        """Return the owner's available care time in minutes."""
        raise NotImplementedError


@dataclass
class Task:
    """A single pet care activity to be scheduled."""

    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    description: str = ""
    pet: Pet | None = None

    def priority_score(self) -> int:
        """Return a numeric score used to rank this task."""
        raise NotImplementedError

    def describe(self) -> str:
        """Return a human-readable summary of the task."""
        raise NotImplementedError


@dataclass
class ScheduledItem:
    """A task placed at a specific start time in the daily plan."""

    start_time: str  # "HH:MM"
    task: Task

    def describe(self) -> str:
        """Return a one-line summary, e.g. '08:00 — Morning walk (20 min)'."""
        raise NotImplementedError


class Scheduler:
    """Manages tasks and builds a daily plan from the owner's constraints."""

    def __init__(self, owner: Owner, tasks: list[Task] | None = None) -> None:
        self.owner = owner
        self.tasks: list[Task] = tasks if tasks is not None else []

    def add_task(self, task: Task) -> None:
        """Add a task to the pool of candidate tasks."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a task from the candidate pool."""
        raise NotImplementedError

    def sort_tasks(self) -> list[Task]:
        """Return tasks ordered by scheduling priority."""
        raise NotImplementedError

    def generate_schedule(self, start_time: str = "08:00") -> list[ScheduledItem]:
        """Select and order tasks into a daily plan within available time."""
        raise NotImplementedError

    def explain(self) -> str:
        """Explain why each task was chosen and when it was placed."""
        raise NotImplementedError
