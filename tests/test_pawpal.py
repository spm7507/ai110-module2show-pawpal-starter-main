"""Simple unit tests for the PawPal+ domain model."""

from pawpal_system import Pet, Task


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
