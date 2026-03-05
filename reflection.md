# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**Bug #1: Message Reversal** - When I input 1 as a guess on Normal difficulty and the secret was higher, the game kept telling me "📈 Go HIGHER!" when it should have said "📉 Go LOWER!". Expected: directional guidance matching the comparison (guess > secret = go lower). Actual: reversed messages sending me the opposite direction.

**Bug #2: Type Mismatch Comparison** - On even-numbered attempts, the secret number was silently converted to a string before comparing with the integer guess. This caused string comparison logic (`"1" > "50"` returns False) instead of numeric comparison. Expected: consistent numeric comparison every time. Actual: alternating between numeric and string comparisons based on attempt parity.

**Bug #3: Difficulty Range Bug** - The difficulty ranges were backwards. Normal difficulty allowed 1-100 and Hard allowed 1-50. Expected: Normal should be 1-50, Hard should be 1-100 to match difficulty progression. Actual: easier difficulty had larger range than harder difficulty.

**Bug #4: Form Submission** - Pressing Enter in the text input field didn't submit the guess; you had to click the "Submit Guess" button. Expected: Enter key to submit (standard form behavior). Actual: required explicit button click.

**Bug #5: New Game Reset** - Clicking "New Game" only reset attempts and secret number, but left status as "won" or "lost". Expected: a fresh game state with all variables reset. Actual: clicking the button showed "You already won" message because status wasn't reset.

---

## 2. How did you use AI as a teammate?

**AI Tool Used:** GitHub Copilot (Claude Haiku model) via VS Code chat interface.

**Correct AI Suggestion #1: Message Reversal Fix** - I described the bug ("when I input 1, it says go lower") and Copilot immediately located the `check_guess()` function, identified the reversed emoji/message pairs, and correctly diagnosed that "if guess > secret" should return "Go LOWER!" not "Go HIGHER!". Verification: After swapping the messages and testing with guess=60 secret=50, the game correctly displayed "📉 Go LOWER!" message. Then tested with guess=1 secret=50 and confirmed it now says "📈 Go HIGHER!".

**Correct AI Suggestion #2: Refactoring to logic_utils.py** - Copilot suggested moving `check_guess()`, `parse_guess()`, `get_range_for_difficulty()`, and `update_score()` from app.py into logic_utils.py, then importing them. This separated UI code from game logic cleanly. Verification: After refactoring, the code still ran correctly, and I was able to write pytest tests in tests/test_game_logic.py that imported from logic_utils and all 27 tests passed.

**Misleading AI Suggestion: File Editing Approach** - When I asked Copilot to remove the duplicate function definitions from app.py after refactoring, it suggested using `replace_string_in_file` to edit specific sections. However, the file had become corrupted with mixed content during the replacement, causing the code to be malformed. The tool suggested approach didn't account for the file's current state. Verification: I detected this was wrong because the file displayed syntax errors within the editor, showing orphaned code like `if difficulty == "Easy"` without the function definition. I recovered by using a terminal command `cat > app.py` to recreate the file cleanly with all correct imports and structure.

---

## 3. Debugging and testing your fixes

**How I Verified Fixes:** I used two strategies - manual gameplay testing in the Streamlit app and automated pytest tests. For manual testing, I checked each bug by playing the game: inputting specific numbers (like 1 when secret was higher) to verify the directional message was now correct. For range bugs, I switched difficulty levels and observed the sidebar display the correct ranges. I ran the game multiple times on each difficulty to confirm the ranges matched expectations.

**Manual Test Example - Message Reversal:** After fixing the reversed messages, I tested by guessing 100 when the secret was 50 (on Normal: 1-50 range). The game now correctly showed "📉 Go LOWER!" message, confirming the fix worked. I then tested the opposite: guess 1 when secret was 40, and it showed "📈 Go HIGHER!" as expected.

**Automated Test Example with pytest:** I created 27 pytest tests targeting each bug. For the message reversal bug, I wrote `test_check_guess_too_high_message()` which calls `check_guess(60, 50)` and asserts the message contains "Go LOWER!". Running `pytest tests/test_game_logic.py -v` showed all 27 tests passed, including tests for difficulty ranges (`test_difficulty_normal_range()` checks Normal returns 1-50, `test_difficulty_hard_range()` checks Hard returns 1-100). The pytest results provided objective verification that all comparison logic, scoring, and parsing functions work correctly.

**AI's Role in Testing:** When pytest initially failed with `ModuleNotFoundError: No module named 'logic_utils'`, Copilot suggested adding the parent directory to sys.path in the test file. This was correct - the fix allowed pytest to find the logic_utils module and all tests ran successfully. Copilot also helped me structure the tests with clear comments explaining which bug each test targets.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

---

## Commit Message Summary

**To generate a commit message:** Open the Source Control tab in VS Code, stage your changes, click the Copilot sparkle icon next to the commit message input, and let Copilot compose a summary message like:

```
Fix game glitches: reverse messages, fix type comparison, swap difficulty ranges, add form submission, reset game state

- Swap message directions in check_guess() (was "go lower" when too high)
- Remove type conversion on even attempts (was causing string comparison bugs)
- Correct difficulty ranges: Normal 1-50, Hard 1-100 (was reversed)
- Wrap guess form in st.form() to enable Enter key submission
- Complete session state reset on new game (status, attempts, score, history)
- Refactor game logic into logic_utils.py for better separation of concerns
- Add comprehensive pytest suite with 27 tests verifying all fixes
```
