import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", task_type="exercise", priority="high",
                status="pending", duration_minutes=30, due_time="07:00")
    task.mark_complete()
    assert task.status == "complete"


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(title="Feeding", task_type="feeding", priority="medium",
                status="pending", duration_minutes=10, due_time="08:00")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1
