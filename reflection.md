# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My intital UML desgin focused on creating different classes for owner, tasks, and the schedule. The goal for my UML desgin is to make the app is the tasks, and schedule is easy to the follow the data that the pet owner gave. 



- What classes did you include, and what responsibilities did you assign to each?

1. Pet Class: stores information about the pet
2. Owner Class: stores information about the owner 
3. Task Class: stores information of the task that the owner added
4. Scheduler Class: generates a schedule by roting tasks on the time.

**b. Design changes**

- Did your design change during implementation?

Yes, my design changed a bit during implementation.

- If yes, describe at least one change and why you made it.

The one change that I made is that I created Task class to manage all the tasks that was happening. Before all the tasks belonged to Pet class.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The one tradeoff my scheduler makes is it sorts tasks by priority.Once it sorts the tasks than it starts listing thw place of each which can fit in the owner's remaining time. 



- Why is that tradeoff reasonable for this scenario?

The tradeoff is reasonable for this scenario because priority matters more than fitting. The highest priority must be schedule first so nothing would happen to the pets.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
