"""PawPal+ demo: build a small care plan and print today's schedule."""

from datetime import datetime

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


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

    # Add at least three tasks with different durations/priorities.
    scheduler = Scheduler(owner)
    scheduler.add_task(
        Task("Morning walk", duration_minutes=30, priority=Priority.HIGH, pet=rex)
    )
    scheduler.add_task(
        Task("Give medication", duration_minutes=10, priority=Priority.HIGH, pet=whiskers)
    )
    scheduler.add_task(
        Task("Feed breakfast", duration_minutes=15, priority=Priority.MEDIUM, pet=rex)
    )
    scheduler.add_task(
        Task("Play time", duration_minutes=20, priority=Priority.LOW, pet=whiskers)
    )

    # Print today's schedule, starting at 08:00.
    print("Today's Schedule")
    print("================")
    for item in scheduler.generate_schedule(start_time="08:00"):
        print(f"{to_ampm(item.start_time)} — {item.task.describe()}")


if __name__ == "__main__":
    main()
