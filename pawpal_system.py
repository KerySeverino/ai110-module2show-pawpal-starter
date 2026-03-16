from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    task_type: str
    priority: str
    status: str
    duration_minutes: int
    due_time: str

    def is_high_priority(self) -> bool:
        pass

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_title: str) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_name: str) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass


class Scheduler:
    def __init__(self) -> None:
        self.scheduled_tasks: List[Task] = []

    def schedule_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass
