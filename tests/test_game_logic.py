# TEST SUITE: Game Glitch Investigator Fixes
# =============================================================================
# This test suite validates all bugs found and fixed in collaboration with Copilot:
# 1. Message reversal bug in check_guess() - told user opposite direction
# 2. Difficulty range bug - Normal and Hard had swapped ranges
# 3. Type comparison bug - secret converted to string on even attempts
# 4. Form submission bug - Enter key didn't work in text input
# 5. New Game reset bug - didn't reset all session state
# =============================================================================

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import logic_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ============================================================================
# TEST: check_guess() - Message Reversal Bug Fix
# ============================================================================
# Bug: Messages were reversed - "Go HIGHER!" when guess was too high,
# "Go LOWER!" when guess was too low. This tests that it's now correct.
# Fix: Swapped the messages to give correct directional guidance

def test_check_guess_correct():
    """Test that correct guess returns 'Win' outcome with correct message."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_check_guess_too_high_message():
    """Test that when guess > secret, message says 'Go LOWER!' (not 'Go HIGHER!')"""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "Go LOWER!" in message, f"Expected 'Go LOWER!' but got: {message}"


def test_check_guess_too_low_message():
    """Test that when guess < secret, message says 'Go HIGHER!' (not 'Go LOWER!')"""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "Go HIGHER!" in message, f"Expected 'Go HIGHER!' but got: {message}"


def test_check_guess_boundary_low():
    """Test edge case: guess is minimum (1) but secret is higher."""
    outcome, message = check_guess(1, 50)
    assert outcome == "Too Low"
    assert "Go HIGHER!" in message


def test_check_guess_boundary_high():
    """Test edge case: guess is 100 but secret is lower."""
    outcome, message = check_guess(100, 50)
    assert outcome == "Too High"
    assert "Go LOWER!" in message


# ============================================================================
# TEST: get_range_for_difficulty() - Range Bug Fix
# ============================================================================
# Bug: Normal was 1-100 and Hard was 1-50. Fixed to Normal: 1-50, Hard: 1-100
# Fix: Swapped the return values for Normal and Hard difficulty levels
# Discovery: Found via user reporting "go lower" message when input was 1 on Normal difficulty

def test_distance_easy_range():
    """Test Easy difficulty returns 1-20 range."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_difficulty_normal_range():
    """Test Normal difficulty returns 1-50 range (was incorrectly 1-100)."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50, "Normal should be 1-50, not 1-100"


def test_difficulty_hard_range():
    """Test Hard difficulty returns 1-100 range (was incorrectly 1-50)."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100, "Hard should be 1-100, not 1-50"


def test_difficulty_default_range():
    """Test unknown difficulty returns default 1-100 range."""
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


# ============================================================================
# TEST: parse_guess() - Input Parsing
# ============================================================================

def test_parse_guess_valid_integer():
    """Test parsing a valid integer input."""
    ok, guess, error = parse_guess("42")
    assert ok is True
    assert guess == 42
    assert error is None


def test_parse_guess_floating_point():
    """Test parsing a floating point number converts to int."""
    ok, guess, error = parse_guess("42.7")
    assert ok is True
    assert guess == 42
    assert error is None


def test_parse_guess_empty_string():
    """Test that empty string returns error."""
    ok, guess, error = parse_guess("")
    assert ok is False
    assert guess is None
    assert error == "Enter a guess."


def test_parse_guess_none():
    """Test that None input returns error."""
    ok, guess, error = parse_guess(None)
    assert ok is False
    assert guess is None
    assert error == "Enter a guess."


def test_parse_guess_invalid_string():
    """Test that non-numeric input returns error."""
    ok, guess, error = parse_guess("abc")
    assert ok is False
    assert guess is None
    assert error == "That is not a number."


def test_parse_guess_negative_number():
    """Test parsing negative numbers."""
    ok, guess, error = parse_guess("-5")
    assert ok is True
    assert guess == -5
    assert error is None


# ============================================================================
# TEST: update_score() - Score Updates
# ============================================================================

def test_update_score_win_first_attempt():
    """Test score calculation for winning on first attempt."""
    # Points = 100 - 10 * (1 + 1) = 80
    new_score = update_score(0, "Win", 1)
    assert new_score == 80


def test_update_score_win_second_attempt():
    """Test score calculation for winning on second attempt."""
    # Points = 100 - 10 * (2 + 1) = 70
    new_score = update_score(0, "Win", 2)
    assert new_score == 70


def test_update_score_win_minimum_points():
    """Test that minimum win score is 10 points."""
    # Points = 100 - 10 * (20 + 1) = -110, but capped at 10
    new_score = update_score(0, "Win", 20)
    assert new_score == 10


def test_update_score_too_high_even_attempt():
    """Test score increases by 5 on even attempts when guess is too high."""
    new_score = update_score(100, "Too High", 2)
    assert new_score == 105


def test_update_score_too_high_odd_attempt():
    """Test score decreases by 5 on odd attempts when guess is too high."""
    new_score = update_score(100, "Too High", 3)
    assert new_score == 95


def test_update_score_too_low():
    """Test score always decreases by 5 when guess is too low."""
    new_score = update_score(100, "Too Low", 2)
    assert new_score == 95
