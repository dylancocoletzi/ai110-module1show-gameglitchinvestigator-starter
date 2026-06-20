# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.

The game is a number-guessing game built with Streamlit. The player picks a difficulty (Easy, Normal, or Hard), which sets the number range and how many attempts they get. The app picks a secret number, and the player guesses until they either find it or run out of attempts. After each guess the game gives a "higher" or "lower" hint, tracks the score, and shows a history of past guesses in a Developer Debug Info panel.

- [x] Detail which bugs you found.

1. **Difficulty didn't update the game.** The main page always said "between 1 and 100" and the secret number wasn't generated within the chosen difficulty's range (it was only created once on first load).
2. **The hints were backwards.** A guess that was too low told me to "go LOWER" and a guess that was too high told me to "go HIGHER" — the directions were swapped.
3. **The attempts-left counter was off by one.** A fresh game started the count at 1 instead of 0, so it showed one fewer attempt than the difficulty allowed.
4. **Invalid guesses still cost an attempt.** The counter increased before checking whether the input was even a number.
5. **Pressing Enter dropped the guess.** Because the input wasn't in a form, hitting Enter re-ran the app without submitting, so the guess wasn't stored and attempts didn't change.
6. **The Developer Debug Info lagged one guess behind.** The panel was drawn before the guess was processed, so the first guess looked like it was never logged.
7. **"New Game" didn't fully reset.** It kept the old history and score and left the "Game over..." status on screen.
8. **Changing difficulty didn't reset the game state** either — it rolled a new secret but kept the old history, attempts, and score.

- [x] Explain what fixes you applied.

1. **Difficulty:** track which difficulty the secret was made for and re-roll it (within `low`/`high`) whenever the difficulty changes, and use `low`/`high` in the on-screen text and in "New Game" instead of hardcoding 1–100.
2. **Hints:** swapped the "go HIGHER"/"go LOWER" messages back to the correct directions in `check_guess` (including the backup branch).
3. **Attempts counter:** initialize `attempts` to 0 so a fresh game shows the full attempt limit.
4. **Enter key:** wrapped the guess input and submit button in an `st.form` so pressing Enter submits like clicking the button.
5. **Debug panel lag:** moved the guess-processing code above the live state/debug display so they always reflect the most recent guess.
6. **Resets:** made both "New Game" and changing difficulty reset all per-game state (attempts, history, score, and status), so each starts a truly fresh game.
7. **Refactor:** moved the core logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) into `logic_utils.py`, keeping `app.py` focused on the UI.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects "Hard" difficulty in the sidebar → the main page updates to show the correct range (1–50) and 5 attempts left.
2. User enters a guess of 40 → game returns "Go LOWER" because the guess is too high.
3. User enters a guess of 20 → game returns "Go HIGHER" because the guess is too low.
4. After each guess, the attempts-left counter goes down by one, the score updates, and the guess appears in the Developer Debug Info history.
5. User enters the correct number → the game shows a win message with the secret and final score, and the game ends.
6. User clicks "New Game" → history, score, and status all reset, and a fresh secret is generated within the chosen difficulty's range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
