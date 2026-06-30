import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

PRIORITY_MAP = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

# --- session "vault": create the domain objects once, reuse across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.subheader("Owner & Pets")
owner.name = st.text_input("Owner name", value=owner.name)
owner.set_availability(
    int(st.number_input("Available minutes today", min_value=0, max_value=1440, value=120))
)

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("Age (years)", min_value=0, max_value=40, value=3)

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species, age=int(pet_age)))

if owner.pets:
    st.write("Pets:")
    for pet in owner.pets:
        st.write(f"- {pet.describe()} — {pet.task_count()} task(s)")
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Each task is scheduled and (optionally) attached to a pet.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

pet_choices = ["(none)"] + [pet.name for pet in owner.pets]
assign_to = st.selectbox("Assign to pet", pet_choices)

if st.button("Add task"):
    chosen_pet = next((pet for pet in owner.pets if pet.name == assign_to), None)
    task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=PRIORITY_MAP[priority],
        pet=chosen_pet,
    )
    scheduler.add_task(task)
    if chosen_pet is not None:
        chosen_pet.add_task(task)

if scheduler.tasks:
    st.write("Current tasks:")
    for task in scheduler.tasks:
        st.write(f"- {task.describe()}")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Calls the scheduler to fit tasks into the owner's available time.")

if st.button("Generate schedule"):
    schedule = scheduler.generate_schedule()
    if schedule:
        for item in schedule:
            st.write(item.describe())
    else:
        st.info("Nothing scheduled — no tasks fit the available time.")
    st.text(scheduler.explain())
