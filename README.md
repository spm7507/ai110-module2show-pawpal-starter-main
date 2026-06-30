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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule
================
08:00 AM — Give medication (10 min) [priority: high] for Whiskers
08:10 AM — Morning walk (30 min) [priority: high] for Rex
08:40 AM — Feed breakfast (15 min) [priority: medium] for Rex
08:55 AM — Play time (20 min) [priority: low] for Whiskers


```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

Each scheduling feature and the method in `pawpal_system.py` that implements it:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Priority sorting** | `Scheduler.sort_tasks()` | Orders tasks by `Task.priority_score()` (priority first, shorter duration as tie-breaker). |
| **Time sorting (tasks)** | `Scheduler.sort_tasks_by_time()` | Orders tasks by their `Task.time` attribute; untimed tasks sort last. |
| **Time sorting (schedule)** | `Scheduler.sort_by_time()` | Orders generated `ScheduledItem`s chronologically by start time. |
| **Filtering by pet / status** | `Scheduler.filter_tasks(pet=, pet_name=, completed=)` | Narrows the task pool by pet object, case-insensitive pet name, and/or completion status. |
| **Schedule building** | `Scheduler.generate_schedule()` | Greedy fit: places highest-priority tasks that fit the owner's available minutes; skips completed tasks by default. |
| **Conflict detection** | `Scheduler.find_conflicts()` | Returns overlapping `ScheduledItem` pairs as `Conflict`s; `Conflict.same_pet` flags same-pet vs. cross-pet clashes. |
| **Conflict reporting** | `Scheduler.detect_conflicts()`, `Scheduler.explain_conflicts()` | Raw `(earlier, later)` pairs, and a human-readable multi-line report. |
| **Lightweight conflict warning** | `Scheduler.conflict_warning()` | Returns a one-line warning string (or `None` if clear) and never raises — safe for UI use. |
| **Recurring tasks (within a day)** | `Task.is_recurring()`, `Scheduler.generate_schedule()` | `interval_minutes` + `occurrences` repeat a task several times in one day (e.g. meds every 8h). |
| **Recurring tasks (daily / weekly)** | `Task.next_occurrence()`, `Scheduler.complete_task()` | Completing a `recurrence="daily"`/`"weekly"` task auto-creates the next dated instance. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
