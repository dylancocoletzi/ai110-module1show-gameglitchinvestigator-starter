# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The first time I ran it, it looked like a normal number-guessing game: a sidebar to pick a difficulty (Easy/Normal/Hard), a box to type a guess, and hints telling me to go higher or lower. Pretty quickly things felt "off." The sidebar said each difficulty had its own range and attempt limit, but the main page always said "between 1 and 100" and didn't actually match the difficulty I picked. The attempts-left counter also looked wrong from the start (it showed one fewer attempt than the difficulty allowed), and when I made guesses the hints sometimes pointed me the wrong direction. So it ran without crashing, but almost every piece of game logic behaved inconsistently.
- List at least two concrete bugs you noticed at the start  
1. The difficulty setting didn't actually change the game. The sidebar showed each difficulty's range and attempt limit, but the main page always said "between 1 and 100" and the secret number never updated to the new range when I switched difficulty (it was only generated once on the first load).
2. The hints were backwards. When the secret was 89 and I guessed 80, the game told me to "go LOWER" when it should have said "go HIGHER" — the higher/lower direction was inverted.
3. The attempts-left counter was off by one. On a fresh game (for example Hard, which allows 5 attempts) it showed 4 left before I had even guessed, because the count started at 1 instead of 0.
4. Invalid guesses still cost an attempt. Because the counter increased before checking if the input was valid, typing something that wasn't a number still used up a turn.
5. Some guesses seemed to be ignored. If I pressed Enter instead of clicking "Submit Guess," the guess wasn't stored in the history and the attempts didn't go down — it turned out the input wasn't inside a form, so Enter just reran the app without submitting.
6. The Developer Debug Info lagged one guess behind. After my first guess, the history still looked empty and the attempts count didn't update, because the debug panel was drawn before the guess was processed.
7. "New Game" didn't fully reset. Starting a new game kept the old history and score, and the "Game over..." text stayed on screen, because only the secret and attempts were reset (history, score, and status were not).
8. Changing difficulty also didn't reset the game state. Switching difficulty rolled a new secret but kept the old history, attempts, and score, so the Developer Debug Info never cleared.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Select "Hard" difficulty | Main page shows range 1–50 and secret is within 1–50 | Main page still says "between 1 and 100" and the secret stays in the old range | None |
| Secret is 89, guess 80 | Hint: "Go HIGHER" | Hint: "Go LOWER" (direction inverted) | None |
| Fresh game on Hard (5 attempts), before guessing | Attempts left: 5 | Attempts left: 4 (counter started at 1) | None |
| Type "abc" (not a number) and submit | Error shown, attempt NOT used | Error shown but attempts left still decreased | None |
| Type 50 and press Enter | Guess is submitted, stored in history, attempts decrease | Nothing happens — guess not stored, attempts unchanged | None |
| Make the first guess | History shows the guess and attempts update | Debug panel still shows empty history / old attempts (one guess behind) | None |
| Click "New Game" after losing | Fresh game: empty history, score 0, game active | Old history and score kept, "Game over..." text stays, can't guess | ...Start a new game to try again. |
| Change difficulty mid-game | Fresh game and Developer Debug Info cleared | New secret rolled but old history, attempts, and score remain | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used two AI tools for this project. The main one was Claude Code inside VS Code, which I worked with directly to investigate the buggy game logic. I would describe a bug I noticed (like the hints being backwards or the difficulty not updating the main page), and Claude would help me pinpoint exactly where in the code it happened, explain why, and then fix it once I confirmed the approach — usually leaving a comment explaining what was broken and how we fixed it. I also used ChatGPT separately to help me refine and clean up my written answers to these reflection questions so they were clearer and easier to read.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I noticed the hints were backwards — when the secret was 89 and I guessed 80, the game told me to "go LOWER" instead of "go HIGHER." The AI traced it to the check_guess function and explained that the two hint messages were simply swapped: a guess that was too high should say "go LOWER" and a guess that was too low should say "go HIGHER." It also pointed out the same swap existed in a backup branch of the function. After we swapped the messages back, I verified the fix by running check_guess with a few values: guess 80 vs secret 89 now returned "Go HIGHER," guess 95 vs 89 returned "Go LOWER," and a matching guess returned "Correct," so I knew the directions were finally right.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I said that sometimes a guess wasn't being stored in the history, the AI suggested the problem was that decimal guesses were being rounded down (for example, "8.9" became 8 in parse_guess), and it marked that line as the bug. This was misleading because rounding wasn't actually why a guess looked missing — the guess was still being stored, just as a whole number — so it didn't match the bug I was describing. I verified this by realizing the value still showed up in the history, just changed, which meant nothing was truly being dropped. I told the AI to revert that change, and it removed the comment so we could keep looking for the real cause (which turned out to be the Enter key not submitting and the debug panel lagging one guess behind).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was fixed by reproducing the exact situation that triggered it and checking that it now behaved the way I expected. For example, after fixing the hints I re-ran the scenario where the secret was 89 and I guessed 80, and made sure it now said "Go HIGHER." For the Streamlit bugs I tested in the running app — switching difficulty, starting a new game, and pressing Enter — and watched the Developer Debug Info to confirm the history, attempts, and score updated correctly. I only moved on once the original symptom was gone and nothing else had broken.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I wrote pytest tests for the logic in logic_utils.py, including two that target the inverted-hint bug: one checks that check_guess(80, 89) returns a "Go HIGHER" message and another that check_guess(95, 89) returns "Go LOWER." Running them showed something useful right away — the original starter tests were failing because they compared check_guess to a plain string like "Win," but the function actually returns a tuple (outcome, message). That told me the tests and the code didn't agree on the return shape, so I updated the tests to unpack the tuple, and then all 15 tests passed.

- Did AI help you design or understand any tests? How?
Yes. The AI helped me see that the existing tests were failing because of the tuple-vs-string mismatch, and it explained why I couldn't just change check_guess to return a single string (the app unpacks both the outcome and the message). It also suggested writing tests that check the hint message direction, not just the outcome label, since the bug I fixed was specifically in the message text. That helped me understand that a good test should target the exact behavior that was broken.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I would explain that every time you interact with a Streamlit app — clicking a button, typing in a box, changing a dropdown — Streamlit re-runs the entire script from top to bottom, like refreshing the page. Because of that, any normal variable gets reset on each rerun, so it can't remember anything between interactions. Session state is the fix: it's like a little backpack the app carries between reruns, where you store things you want to keep, like the secret number, the score, or the guess history. Working on this project, two of the bugs came straight from misunderstanding this — the Developer Debug Info showed old values because it was drawn before the new guess was saved on that rerun, and pressing Enter "lost" a guess because that rerun happened without actually submitting. So the big lesson is that order matters: you have to update session state before you display it, and you have to control when a rerun actually processes the user's input.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
One habit I want to reuse is fixing one bug at a time and confirming it before moving on. Instead of trying to fix everything at once, I would describe a single bug, have the AI mark exactly where it was happening and explain why, and then test that one fix before starting the next. This kept the changes small and easy to follow, and it meant I always understood what each fix actually did instead of just trusting it.

- What is one thing you would do differently next time you work with AI on a coding task?
Next time I would describe the bug I'm seeing more precisely up front, including the exact steps to reproduce it and what I expected to happen. When I told the AI a guess "wasn't being stored," it guessed the wrong cause (the decimal rounding) and marked the wrong line, which sent us down a small detour. Being clearer about what I actually observed would help the AI find the real cause faster and avoid misleading suggestions.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project showed me that AI-generated code can look polished and "production-ready" while still being full of subtle logic bugs. It made me realize I have to read, test, and verify AI code myself rather than assuming it works just because it runs without crashing.
