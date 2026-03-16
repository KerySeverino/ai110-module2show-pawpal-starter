# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

Phase 4 added several improvements to how PawPal+ handles tasks:

- **Sorting by due date and time** — the schedule is now ordered by `(due_date, due_time)` so tasks appear in true chronological order across multiple days.
- **Filtering by status** — owners can view only `pending` or `complete` tasks to stay focused on what still needs doing.
- **Filtering by pet** — tasks can be scoped to a single pet, useful when managing care schedules for multiple animals.
- **Recurring tasks** — tasks can be set to repeat `daily` or `weekly`. When a recurring task is marked complete, the next occurrence is automatically created and added to that pet's schedule.
- **Conflict detection** — any two tasks sharing the same `(due_date, due_time)` are flagged with a warning so the owner can reschedule before the conflict becomes a problem.
