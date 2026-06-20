import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIXED: track which difficulty the secret was generated for, and re-roll it
# whenever the difficulty changes so the secret always matches the chosen range.
if "secret" not in st.session_state or st.session_state.get("secret_difficulty") != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.secret_difficulty = difficulty

# FIXED: start attempts at 0 (no guesses made yet) so "Attempts left" shows the
# full attempt_limit on a fresh game, matching how New Game initializes it.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# FIXED: use the computed low/high so the main page reflects the chosen
# difficulty. The range prompt is static (recomputed every run) so it can stay
# here; the live "Attempts left" counter and debug panel moved below the submit
# handler — see the Option B fix — so they reflect the guess just processed.
st.info(f"Guess a number between {low} and {high}.")

# FIXED: wrap the guess input and its submit button in an st.form. A
# form_submit_button returns True both when clicked AND when Enter is pressed
# inside the form, so guesses entered via Enter are no longer silently dropped.
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # BUG: New Game only reset attempts and secret, leaving history, score, and
    # status untouched. So the debug panel kept the old guesses/score and, because
    # status stayed "won"/"lost", the "Game over..." text persisted and the new
    # game was still blocked from accepting guesses.
    # FIXED: reset ALL per-game state so a new game starts truly fresh.
    st.session_state.attempts = 0
    # FIXED: use low/high so a new game uses the range of the chosen difficulty.
    st.session_state.secret = random.randint(low, high)
    st.session_state.secret_difficulty = difficulty
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.success("New game started.")
    st.rerun()

# FIXED (Option B): capture whether the game was already over BEFORE processing
# this run's guess. Used to guard the submit handler and to decide whether to
# show the persistent game-over reminder (so we don't double up on the turn the
# game actually ends).
game_already_over = st.session_state.status != "playing"

# FIXED (Option B): process the guess HERE, before rendering the live state and
# debug panel below. Previously those were drawn above this block, so they always
# lagged one guess behind — the first guess looked like it was never logged.
if submit and not game_already_over:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# FIXED (Option B): live game state, rendered AFTER the guess is processed so it
# is always current (no more one-guess lag). Also renders on the game-over screen
# now, since the st.stop() above was removed in favor of guarding the handler.
st.caption(f"Attempts left: {attempt_limit - st.session_state.attempts}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# Persistent reminder only when the game was already over coming into this run,
# so the turn the game ends shows just the win/loss message from the handler.
if game_already_over:
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
