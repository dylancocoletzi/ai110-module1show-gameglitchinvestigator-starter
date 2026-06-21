from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

# NOTE: check_guess returns a tuple (outcome, message), so we unpack it.
# The bugs that live in app.py (attempts off-by-one, Enter-to-submit, the debug
# panel lagging a guess behind, and New Game / difficulty not resetting state)
# depend on Streamlit session_state and reruns, so they are verified manually
# rather than in these pure-logic unit tests.


# --- check_guess: outcome labels (existing tests, updated to unpack the tuple) ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- check_guess: inverted-hint bug ------------------------------------------

def test_hint_too_low_tells_player_to_go_higher():
    # Targets the inverted-hint bug: secret 89, guess 80 is TOO LOW, so the
    # hint must tell the player to go HIGHER (before the fix it said "Go LOWER").
    outcome, message = check_guess(80, 89)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hint_too_high_tells_player_to_go_lower():
    # Targets the inverted-hint bug: a guess that is TOO HIGH must tell the
    # player to go LOWER (before the fix it said "Go HIGHER").
    outcome, message = check_guess(95, 89)
    assert outcome == "Too High"
    assert "LOWER" in message


# --- get_range_for_difficulty: difficulty bug --------------------------------

def test_difficulty_ranges():
    # Each difficulty maps to its own range; this is what the main page and the
    # secret number must use instead of a hardcoded 1-100.
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_difficulty_unknown_defaults_to_full_range():
    # Any unrecognized difficulty falls back to the full 1-100 range.
    assert get_range_for_difficulty("???") == (1, 100)


# --- parse_guess: input handling ---------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_string_is_invalid():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_none_is_invalid():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None


def test_parse_non_number_is_invalid():
    # A non-numeric guess is rejected rather than crashing.
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_decimal_is_truncated():
    # Documents current behavior: a decimal guess is accepted but truncated to
    # an int (e.g. "8.9" -> 8). Kept as-is since we reverted changing this.
    ok, value, err = parse_guess("8.9")
    assert ok is True
    assert value == 8


# --- update_score ------------------------------------------------------------

def test_winning_score_increases():
    # A win should add points to the current score.
    new_score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert new_score > 0


def test_winning_score_has_minimum_of_ten():
    # Even after many attempts a win never awards fewer than 10 points.
    new_score = update_score(current_score=0, outcome="Win", attempt_number=20)
    assert new_score == 10


def test_too_low_loses_points():
    # A "Too Low" outcome subtracts points.
    new_score = update_score(current_score=50, outcome="Too Low", attempt_number=1)
    assert new_score == 45
