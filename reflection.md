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

The one tradeoff my scheduler makes is it sorts tasks by priority.Once it sorts the tasks than it starts listing the place of each which can fit in the owner's remaining time. 



- Why is that tradeoff reasonable for this scenario?

The tradeoff is reasonable for this scenario because priority matters more than fitting. The highest priority must be schedule first so nothing would happen to the pets.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

The AI tools during this projects help me to draft my ideas. Than I was also able to implment the ideas into my code as well. I was also able to ask suggest as well. 

- What kinds of prompts or questions were most helpful?

THe prompt that was most helpful for me is Use your AI coding assistant's automatic editing or agent mode to flesh out the core implementation of your four classes in pawpal_system.py. I felt like it was very efficent because I didn't had to code from scrtach instead AI coding helped me. All I needed to is check if the code is right.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

 THe one moment where I did not accept an AI suggestion is the example schedule. The schedule didn't make sense so I had to edit the output out. I put the AM/PM in the schedule to make the schedule for sense.


- How did you evaluate or verify what the AI suggested?
  
  In my settings I put ask before edits so that I can check what the bot is editing and see if I like it or not. If not I would edit the code out. Overall this is how I would evaluate or verify what the AI suggested. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested the core behaviors of each class along with a number of edge cases. For tasks, I tested that `mark_complete()` correctly flips a task's status and that adding a task to a pet increases that pet's task count. For the scheduler, I tested its three main jobs: sorting tasks by priority and by preferred time, filtering tasks by pet and by completion status, and generating a daily schedule that fits within the owner's available minutes. I also tested conflict detection — that overlapping tasks are flagged, that back-to-back tasks are not flagged (I treat time ranges as half-open, so a task ending at 08:30 and another starting at 08:30 is fine), and that conflicts are labeled as same-pet vs. cross-pet. On top of that I tested recurring tasks and edge cases like a zero-minute budget, a task that exactly fills the remaining time, a malformed start time, and an empty scheduler with no tasks at all.

- Why were these tests important?

These tests were important because the scheduler is the heart of the app, and a bug there would give the pet owner a wrong or unsafe plan — for example, double-booking two tasks at the same time or dropping a high-priority task like medication. Testing the sorting and budget logic made sure the schedule respects both priority and the owner's real available time. Testing conflict detection mattered because the whole point of the app is to warn the owner when tasks overlap, so I needed to be sure it caught real overlaps without false alarms on back-to-back tasks. The edge-case tests (zero budget, empty inputs, bad time strings) were important because those are exactly the situations that crash an app if they aren't handled, and testing them gave me confidence the app wouldn't break when a user did something unexpected.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  

Confidence Level:

My confidence level is about a 4.5 all the test passed so I am too worried about but sometimes there is always a loop hole in tests. Overall this is my confidence level for the test results.

- What edge cases would you test next if you had more time?

The cases that I would test if I had time is to see if three or more tasks overlap.



---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

  THe part of this project that I was very satisfied was with was when the tests passed. In the previous project I was having trouble with the pytest. Now I was able to know what a pytest is and how to implent it. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

     I would improve on making a uml better. I felt like I was struggling since it was my first time making a UML. Overall this is what I would improve on with this project.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The one important thing I learned about desgining system is how UML are created!


Reflect on AI Strategy: Specifically describe your experience with your AI coding assistant:

Which AI coding assistant features were most effective for building your scheduler?

The AI coding assistant features were most effective for buliding scheduler is the drafting because then you would know what you are going to do with your code/plan.

Give one example of an AI suggestion you rejected or modified to keep your system design clean.

One example of an AI suggestion I would reject was the output that it gave me for the schedule. It didn't add the AM/PM so I had to implent it. 

How did using separate chat sessions for different phases help you stay organized?

I separate the chats when I had a problem solved or move on with another part of the code.


Summarize what you learned about being the "lead architect" when collaborating with powerful AI tools.

I learned that you always need to have a plan. Therefor eyou would need to creat a UML so you can follow it. Soemtimes you got to change it since plans can change it too.