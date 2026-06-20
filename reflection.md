# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The first time I ran the game, it seemed like a guessing game that gave you hints if your high or lower to the number to guess. I expected the attempts left to decrease after the first guess but it didn't.
- List at least two concrete bugs you noticed at the start  
1. The hints that the game provided are inconsistent. If I guess the same number a few times, the hint would be different. 
2. When you chose what difficulty you want to play the game, it tells you the allowed attempts but it is not consistent with the main page allowed attempts.
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
guess 1 | Attempts left: 6  | Attempts left: 7| None
New Game|  Start new game   | Stuck           | ..Start a new game to try again.
guess 1 |    Go Higher      | Go Lower        | None

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
For this project, the AI tool I used was claude code in VS code to investihate the current buggy logic of some features of the app. 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
