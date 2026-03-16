from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    task_type: str
    priority: str
    status: str
    duration_minutes: int
    due_time: str

    def is_high_priority(self) -> bool:
        """Return True if the task priority is 'high'."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Set the task status to 'complete'."""
        self.status = "complete"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove a task from the list by matching its title."""
        self.tasks = [t for t in self.tasks if t.title != task_title]

    def get_tasks(self) -> List[Task]:
        """Return the list of all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Append a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet from the list by matching its name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pets(self) -> List[Pet]:
        """Return the list of all pets for this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks from all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self) -> None:
        self.scheduled_tasks: List[Task] = []

    def schedule_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by due_time and store them as the current scheduled plan."""
        self.scheduled_tasks = sorted(tasks, key=lambda t: t.due_time)
        return self.scheduled_tasks

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted high-priority first, then medium, then low."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Return all tasks that share a due_time with at least one other task."""
        time_counts = {}
        for task in tasks:
            if task.due_time in time_counts:
                time_counts[task.due_time] += 1
            else:
                time_counts[task.due_time] = 1
        return [t for t in tasks if time_counts[t.due_time] > 1]

    def explain_plan(self) -> str:
        """Return a multi-line string summarizing each task in the current schedule."""
        if not self.scheduled_tasks:
            return "No tasks scheduled yet."
        lines = []
        for task in self.scheduled_tasks:
            line = f"- {task.title} | Due: {task.due_time} | Priority: {task.priority}"
            lines.append(line)
        return "\n".join(lines)
