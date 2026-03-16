import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Initialize session state once ---
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

st.divider()

# --- Step 1: Create Owner (only once) ---
st.subheader("Step 1: Set Up Owner")

owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@example.com")

if st.button("Create Owner"):
    if st.session_state.owner is None:
        st.session_state.owner = Owner(name=owner_name, email=owner_email)
        st.success(f"Owner '{owner_name}' created!")
    else:
        st.info(f"Owner '{st.session_state.owner.name}' already exists.")

st.divider()

# --- Step 2: Add Pets to existing Owner ---
st.subheader("Step 2: Add a Pet")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.warning("Create an owner first.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Pet '{pet_name}' added to {st.session_state.owner.name}.")

st.divider()

# --- Step 3: Add Tasks ---
st.subheader("Step 3: Add a Task")

if st.session_state.owner and st.session_state.owner.get_pets():
    pet_names = [p.name for p in st.session_state.owner.get_pets()]
    selected_pet = st.selectbox("Assign task to", pet_names)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        due_time = st.text_input("Due time (HH:MM)", value="08:00")

    col5, col6 = st.columns(2)
    with col5:
        due_date = st.text_input("Due date (YYYY-MM-DD)", value="2026-03-15")
    with col6:
        recurrence_choice = st.selectbox("Recurrence", ["none", "daily", "weekly"])

    if st.button("Add task"):
        task = Task(
            title=task_title,
            task_type="general",
            priority=priority,
            status="pending",
            duration_minutes=int(duration),
            due_time=due_time,
            due_date=due_date,
            recurrence="" if recurrence_choice == "none" else recurrence_choice,
        )
        for pet in st.session_state.owner.get_pets():
            if pet.name == selected_pet:
                pet.add_task(task)
                break
        st.success(f"Task '{task_title}' added to {selected_pet}.")
else:
    st.info("Add an owner and at least one pet to start adding tasks.")

# --- Show current tasks ---
if st.session_state.owner:
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([{
            "title": t.title,
            "due_date": t.due_date,
            "due_time": t.due_time,
            "priority": t.priority,
            "status": t.status,
            "recurrence": t.recurrence or "—",
        } for t in all_tasks])
    else:
        st.info("No tasks added yet.")
st.divider()

# --- Step 4: Generate Schedule ---
st.subheader("Step 4: Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.warning("Create an owner first.")
    else:
        all_tasks = st.session_state.owner.get_all_tasks()
        if not all_tasks:
            st.warning("Add at least one task before generating a schedule.")
        else:
            st.session_state.scheduler.schedule_tasks(all_tasks)
            st.success("Schedule generated!")
            st.text(st.session_state.scheduler.explain_plan())

            conflicts = st.session_state.scheduler.detect_conflicts(all_tasks)
            if conflicts:
                st.warning("Conflicts detected (same due time):")
                for t in conflicts:
                    st.write(f"- {t.title} at {t.due_date} {t.due_time}")

st.divider()

# --- Phase 4: Filter, Sort & Manage Tasks ---
st.subheader("Phase 4: Filter, Sort & Manage Tasks")

if st.session_state.owner and st.session_state.owner.get_pets():
    scheduler = st.session_state.scheduler

    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by status", ["all", "pending", "complete"])
    with col2:
        pet_options = ["all"] + [p.name for p in st.session_state.owner.get_pets()]
        pet_filter = st.selectbox("Filter by pet", pet_options)

    # Build a (pet, task) list and apply filters
    task_rows = []
    for pet in st.session_state.owner.get_pets():
        if pet_filter != "all" and pet.name != pet_filter:
            continue
        for task in pet.get_tasks():
            task_rows.append((pet, task))

    if status_filter != "all":
        task_rows = [(p, t) for p, t in task_rows if t.status == status_filter]

    # Sort by due_date then due_time
    task_rows.sort(key=lambda x: (x[1].due_date, x[1].due_time))

    # Find conflicting (due_date, due_time) pairs
    all_shown_tasks = [t for _, t in task_rows]
    conflicts = scheduler.detect_conflicts(all_shown_tasks)
    conflict_keys = {(t.due_date, t.due_time) for t in conflicts}

    if not task_rows:
        st.info("No tasks match the current filters.")
    else:
        for pet, task in task_rows:
            status_icon = "✅" if task.status == "complete" else "⏳"
            conflict_flag = " ⚠️ **conflict**" if (task.due_date, task.due_time) in conflict_keys else ""
            recur_label = f" | 🔁 {task.recurrence}" if task.recurrence else ""
            label = (
                f"{status_icon} **{task.title}** — {pet.name} | "
                f"{task.due_date} {task.due_time} | {task.priority}{recur_label}{conflict_flag}"
            )

            col_info, col_btn = st.columns([5, 1])
            with col_info:
                st.markdown(label)
            with col_btn:
                btn_key = f"done_{pet.name}_{task.title}_{task.due_date}"
                if task.status != "complete" and st.button("Mark Done", key=btn_key):
                    task.mark_complete()
                    if task.recurrence:
                        next_task = task.next_occurrence()
                        pet.add_task(next_task)
                        st.success(
                            f"'{task.title}' complete! Next {task.recurrence} occurrence added for {next_task.due_date}."
                        )
                    else:
                        st.success(f"'{task.title}' marked complete.")
                    st.rerun()

    if conflict_keys:
        st.warning(f"{len(conflicts)} task(s) share a due date and time — consider rescheduling.")
else:
    st.info("Add an owner and at least one pet to manage tasks.")
