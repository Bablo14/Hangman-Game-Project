
"""Frequency game logic with improved AI strategies for computer guessing."""
# game_logic.py
import random
import string
from collections import Counter
from config import (
    DIFFICULTIES, POINTS_CORRECT_LETTER, POINTS_WRONG_LETTER,
    POINTS_USE_HINT, POINTS_WIN_BONUS, POINTS_LOSS_PENALTY
)
from scores import get_player_score, set_player_score
from words import CATEGORIES
from questions import pick_question, QUESTIONS as RIDDLE_CATEGORIES

def _get_possible_words(gstate):
    mode = gstate.get("guess_mode", "Direct Guess")
    category = gstate.get("category")
    difficulty = gstate.get("difficulty")
    try:
        if mode == "Question-Based":
            return [q["answer"].lower().replace(" ", "") for q in RIDDLE_CATEGORIES[category][difficulty]]
        else: return CATEGORIES[category][difficulty]
    except (KeyError, IndexError):
        return CATEGORIES["Animals"]["Easy"]

def computer_pick_letter(gstate):
    difficulty = gstate["difficulty"]
    guessed_set = gstate["computer"]["guessed"]
    secret_word = gstate["word"]
    possible_words = _get_possible_words(gstate)
    if difficulty == "Hard":
        hits = {char for char in guessed_set if char in secret_word}
        misses = guessed_set - hits
        filtered_words = [word for word in possible_words if len(word) == len(secret_word) and all(hit in word for hit in hits) and not any(miss in word for miss in misses)]
        if filtered_words:
            all_letters = "".join(filtered_words)
            freq_counter = Counter(all_letters)
            for letter in guessed_set: del freq_counter[letter]
            if freq_counter: return freq_counter.most_common(1)[0][0]
    all_letters = "".join(possible_words)
    if not all_letters: freq_counter = Counter("abcdefghijklmnopqrstuvwxyz")
    else: freq_counter = Counter(all_letters)
    for letter in guessed_set: del freq_counter[letter]
    if not freq_counter:
        for ch in string.ascii_lowercase:
            if ch not in guessed_set: return ch
        return None
    sorted_letters = [item[0] for item in freq_counter.most_common()]
    if difficulty == "Medium":
        top_choices = sorted_letters[:5]
        if top_choices: return random.choice(top_choices)
        elif sorted_letters: return sorted_letters[0]
    if difficulty == "Easy":
        top_choices = sorted_letters[:18]
        random.shuffle(top_choices)
        guess_order = top_choices + sorted_letters[18:]
        for letter in guess_order:
            if letter not in guessed_set: return letter
    for letter in string.ascii_lowercase:
        if letter not in guessed_set: return letter
    return None

def choose_word(category, difficulty):
    try:
        words = CATEGORIES.get(category, {}).get(difficulty, [])
        return random.choice(words) if words else "default"
    except (KeyError, IndexError):
        return "hangman"

def mask_word(word, guessed_letters):
    return " ".join(ch if (not ch.isalpha()) or (ch.lower() in guessed_letters) else "_" for ch in word)

def mask_computer_display(word, computer_guessed_set):
    return " ".join("*" if char.lower() in computer_guessed_set else "_" for char in word if char.isalpha())

def init_single_state(username, difficulty, category, guess_mode, used_words):
    d = DIFFICULTIES[difficulty]
    question_text, word = None, None
    for _ in range(50):
        if guess_mode == "Question-Based":
            q_data = pick_question(category, difficulty)
            potential_word = q_data["answer"].lower().replace(" ", "")
            if potential_word not in used_words:
                word, question_text = potential_word, q_data["q"]
                break
        else:
            potential_word = choose_word(category, difficulty).lower()
            if potential_word not in used_words:
                word = potential_word
                break
    if word is None:
        if guess_mode == "Question-Based":
            q_data = pick_question(category, difficulty)
            word, question_text = q_data["answer"].lower().replace(" ", ""), q_data["q"]
        else:
            word = choose_word(category, difficulty).lower()
    return {
        "mode": "Single Player", "username": username, "difficulty": difficulty,
        "category": category, "multiplier": d["multiplier"], "max_lives": d["lives"],
        "hints_left": d["hints"], "max_hints": d["hints"], "word": word,
        "question_text": question_text, "guessed": set(), "lives_left": d["lives"], 
        "display": mask_word(word, set()), "score_delta": 0, "guess_mode": guess_mode,
        "correct_streak": 0  # NEW: Track correct guess streak
    }

def init_user_vs_user_state(username, difficulty, secret_word):
    d = DIFFICULTIES[difficulty]
    word = "".join(ch.lower() for ch in secret_word.strip() if ch.isalpha())
    return {
        "mode": "User vs User", "username": username, "difficulty": difficulty,
        "category": "Custom", "multiplier": d["multiplier"], "max_lives": d["lives"],
        "hints_left": d["hints"], "max_hints": d["hints"], "word": word,
        "original_secret": secret_word, "question_text": "The secret word was provided by another user.",
        "guessed": set(), "lives_left": d["lives"], "display": mask_word(word, set()),
        "score_delta": 0, "guess_mode": "Direct Guess", "correct_streak": 0
    }

def init_user_vs_computer_state(username, difficulty, category, guess_mode, used_words):
    d = DIFFICULTIES[difficulty]
    question_text, word = None, None
    for _ in range(50):
        if guess_mode == "Question-Based":
            q_data = pick_question(category, difficulty)
            potential_word = q_data["answer"].lower().replace(" ", "")
            if potential_word not in used_words:
                word, question_text = potential_word, q_data["q"]
                break
        else:
            potential_word = choose_word(category, difficulty).lower()
            if potential_word not in used_words:
                word = potential_word
                break
    if word is None:
        if guess_mode == "Question-Based":
            q_data = pick_question(category, difficulty)
            word, question_text = q_data["answer"].lower().replace(" ", ""), q_data["q"]
        else:
            word = choose_word(category, difficulty).lower()
    return {
        "mode": "User vs Computer", "username": username, "difficulty": difficulty,
        "category": category, "multiplier": d["multiplier"], "max_lives": d["lives"],
        "word": word, "question_text": question_text,
        "user": {
            "guessed": set(), "lives_left": d["lives"],
            "display": mask_word(word, set()), "score_delta": 0, 
            "hints_left": d["hints"], "max_hints": d["hints"],
            "correct_streak": 0  # NEW: Track correct guess streak for user
        },
        "computer": {
            "guessed": set(), "lives_left": d["lives"],
            "display": mask_word(word, set()),
        },
        "turn": "user", "guess_mode": guess_mode
    }

def apply_letter_guess(word, guessed_set, lives_left, letter):
    letter = letter.lower()
    if not letter.isalpha() or len(letter) != 1: return 'invalid', guessed_set, lives_left, 0
    if letter in guessed_set: return 'already_guessed', guessed_set, lives_left, 0
    guessed_set.add(letter)
    if letter in word: return 'correct', guessed_set, lives_left, POINTS_CORRECT_LETTER
    else: return 'wrong', guessed_set, lives_left - 1, POINTS_WRONG_LETTER

def use_hint_on(word, display, guessed_set, hints_left):
    if hints_left <= 0: return display, guessed_set, hints_left, 0
    choices = [ch for ch in set(word) if ch.isalpha() and ch not in guessed_set]
    if not choices: return display, guessed_set, hints_left, 0
    pick = random.choice(choices)
    guessed_set.add(pick)
    new_display = mask_word(word, guessed_set)
    return new_display, guessed_set, hints_left - 1, POINTS_USE_HINT

def is_win(display):
    return "_" not in display

def is_loss(lives_left):
    return lives_left <= 0

def finalize_score(username, base_delta, multiplier, did_win):
    total = base_delta + (POINTS_WIN_BONUS if did_win else POINTS_LOSS_PENALTY)
    total = int(total * multiplier)
    prior = get_player_score(username)
    set_player_score(username, prior + total)
    return total, prior + total