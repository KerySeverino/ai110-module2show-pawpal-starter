from pawpal_system import Task, Pet, Owner, Scheduler

# --- Create Owner ---
owner = Owner(name="Jordan", email="jordan@example.com")

# --- Create Pets ---
mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

# --- Create Tasks for Mochi ---
mochi.add_task(Task(title="Morning walk",  task_type="exercise", priority="high",   status="pending", duration_minutes=30, due_time="07:00"))
mochi.add_task(Task(title="Breakfast",     task_type="feeding",  priority="high",   status="pending", duration_minutes=10, due_time="08:00"))
mochi.add_task(Task(title="Evening walk",  task_type="exercise", priority="medium", status="pending", duration_minutes=30, due_time="18:00"))

# --- Create Tasks for Luna ---
luna.add_task(Task(title="Litter box cleaning", task_type="hygiene",  priority="medium", status="pending", duration_minutes=10, due_time="09:00"))
luna.add_task(Task(title="Playtime",            task_type="exercise", priority="low",    status="pending", duration_minutes=15, due_time="15:00"))

# --- Add Pets to Owner ---
owner.add_pet(mochi)
owner.add_pet(luna)

# --- Schedule all tasks ---
scheduler = Scheduler()
all_tasks = owner.get_all_tasks()
scheduler.schedule_tasks(all_tasks)

# --- Print Today's Schedule ---
print("=" * 40)
print("       Today's Schedule for", owner.name)
print("=" * 40)
print(scheduler.explain_plan())
print("=" * 40)

# --- Check for conflicts ---
conflicts = scheduler.detect_conflicts(all_tasks)
if conflicts:
    print("\nConflicts detected:")
    for task in conflicts:
        print(f"  - {task.title} at {task.due_time}")
else:
    print("\nNo scheduling conflicts.")
