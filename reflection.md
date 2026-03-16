# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?


My UML design included four classes: Owner, Pet, Task, and Scheduler. Owner manages pets, Pet stores pet information and its tasks, Task represents actions like feedings or walks, and Scheduler organizes and prioritizes tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.


Yes. I moved most scheduling logic into the Scheduler class instead of keeping it inside Pet. This kept responsibilities clearer and made the design more modular.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Time came first because pet care is deadline-driven, priority and status filtering followed to help owners triage and focus on what still needs doing.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is that conflict detection only checks for exact matches in due date and due time instead of overlapping time ranges. This keeps the logic simpler and easier to understand, even though it does not catch every possible scheduling conflict.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Copilot for inline autocomplete on repetitive patterns (list comprehensions, dataclass boilerplate) and Claude Code chat for design decisions and debugging. Prompts that described the expected behavior in plain English were most effective. Keeping separate chat sessions per phase helped me stay organized.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

AI generated `next_occurrence()` with a ternary that silently treated any unrecognized recurrence string as `"weekly"`. I replaced it with an explicit `if/elif/else` that raises a `ValueError` for unsupported values, so bad input fails loudly instead of producing a wrong result. I verified by tracing through both versions with a bad input value.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion, adding tasks to pets, chronological sorting across dates, recurring task generation, conflict detection, and a pet with no tasks. These cover the core scheduler behaviors — if any of these break, the app stops working correctly for the owner.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence 4/5. The tested behaviors all pass. An untested edge case is a task with an empty `due_date` mixed into a sorted list with dated tasks — empty strings sort before date strings in Python, so undated tasks would always appear first, which may not be intended.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The recurring task logic. When a recurring task is marked complete, `next_occurrence()` automatically computes the next date and the app adds it to the pet's schedule — all in a few clean lines. It was satisfying to see a backend method connect directly to a meaningful UI behavior.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve conflict detection to check for time range overlaps using `due_time + duration_minutes`, not just exact start-time matches. Two tasks at 08:00 and 08:15 with 30-minute durations would not be flagged today, but they would overlap in practice.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Being the "lead architect" means evaluating every AI suggestion critically, not just accepting code that looks correct. AI is good at generating plausible implementations, but it is the developer's responsibility to verify edge cases, check that the design fits the actual requirements, and reject suggestions that are subtly wrong.
