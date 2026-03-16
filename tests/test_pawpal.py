from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    task = Task("Feed", "food", "high", "pending", 10, "08:00")
    task.mark_complete()
    assert task.status == "complete"


def test_add_task_to_pet():
    pet = Pet("Mochi", "dog", 3)
    task = Task("Walk", "exercise", "high", "pending", 30, "08:00")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Walk"


def test_sorting_correctness():
    scheduler = Scheduler()

    task1 = Task("Evening Walk", "exercise", "low", "pending", 20, "18:00", "2026-03-15")
    task2 = Task("Morning Walk", "exercise", "high", "pending", 30, "08:00", "2026-03-15")
    task3 = Task("Vet Visit", "appointment", "high", "pending", 60, "10:00", "2026-03-16")

    sorted_tasks = scheduler.schedule_tasks([task1, task2, task3])

    assert sorted_tasks[0].title == "Morning Walk"
    assert sorted_tasks[1].title == "Evening Walk"
    assert sorted_tasks[2].title == "Vet Visit"


def test_daily_recurrence_creates_next_occurrence():
    task = Task(
        "Morning Walk",
        "exercise",
        "high",
        "pending",
        30,
        "08:00",
        "2026-03-15",
        "daily"
    )

    task.mark_complete()
    next_task = task.next_occurrence()

    assert task.status == "complete"
    assert next_task.title == "Morning Walk"
    assert next_task.status == "pending"
    assert next_task.due_date == "2026-03-16"
    assert next_task.recurrence == "daily"


def test_conflict_detection_flags_duplicate_times():
    scheduler = Scheduler()

    task1 = Task("Feed Mochi", "food", "high", "pending", 10, "08:00", "2026-03-15")
    task2 = Task("Walk Luna", "exercise", "medium", "pending", 20, "08:00", "2026-03-15")
    task3 = Task("Vet Visit", "appointment", "high", "pending", 60, "10:00", "2026-03-15")

    conflicts = scheduler.detect_conflicts([task1, task2, task3])

    assert len(conflicts) == 2
    assert task1 in conflicts
    assert task2 in conflicts


def test_pet_with_no_tasks():
    pet = Pet("Luna", "cat", 5)
    assert pet.get_tasks() == []