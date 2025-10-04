

"""Frequently Updated UI Components"""

# ui_components.py
import customtkinter as ctk
from config import (
    APP_TITLE, LOGO_TEXT, DIFFICULTIES, GUESSING_MODES, TIMER_OPTIONS, NUM_WORDS_OPTIONS
)
from scores import leaderboard, get_player_score, rename_player
from hangman_art import map_progress_to_art
from words import CATEGORIES
from questions import  QUESTIONS as RIDDLE_CATEGORIES
import sounds

# ... (build_start_frame and build_u2u_word_frame are unchanged) ...
def build_start_frame(root, state, on_start_single, on_start_uvu, on_start_uvc, on_refresh, on_reset, on_delete):
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    title = ctk.CTkLabel(frame, text=APP_TITLE, font=("Consolas", 22, "bold"))
    title.pack(pady=(6, 2))
    logo = ctk.CTkLabel(frame, text=LOGO_TEXT, justify="left", font=("Consolas", 12))
    logo.pack(pady=(0, 8))
    user_row = ctk.CTkFrame(frame)
    user_row.pack(fill="x", pady=4)
    ctk.CTkLabel(user_row, text="Username:").pack(side="left", padx=4)
    username_entry = ctk.CTkEntry(user_row)
    username_entry.pack(side="left", padx=4, fill="x", expand=True)
    username_entry.insert(0, state.get("username", ""))
    diff_row = ctk.CTkFrame(frame)
    diff_row.pack(fill="x", pady=4)
    ctk.CTkLabel(diff_row, text="Difficulty:").pack(side="left", padx=4)
    diff_option = ctk.CTkOptionMenu(diff_row, values=list(DIFFICULTIES.keys()), command=lambda choice: sounds.play_sound("click"))
    diff_option.set(state.get("difficulty", "Easy"))
    diff_option.pack(side="left", padx=4)
    num_words_row = ctk.CTkFrame(frame)
    num_words_row.pack(fill="x", pady=4)
    ctk.CTkLabel(num_words_row, text="Number of Words:").pack(side="left", padx=4)
    num_words_option = ctk.CTkOptionMenu(num_words_row, values=list(NUM_WORDS_OPTIONS.keys()), command=lambda choice: sounds.play_sound("click"))
    num_words_option.set(state.get("num_words_label", "Unlimited"))
    num_words_option.pack(side="left", padx=4)
    cat_row = ctk.CTkFrame(frame)
    cat_row.pack(fill="x", pady=4)
    ctk.CTkLabel(cat_row, text="Category:").pack(side="left", padx=4)
    cat_option = ctk.CTkOptionMenu(cat_row, values=list(CATEGORIES.keys()), command=lambda choice: sounds.play_sound("click"))
    cat_option.set(state.get("category", list(CATEGORIES.keys())[0]))
    cat_option.pack(side="left", padx=4)
    def on_guess_mode_change(choice):
        if choice == "Question-Based":
            riddle_cats = list(RIDDLE_CATEGORIES.keys())
            cat_option.configure(values=riddle_cats)
            if cat_option.get() not in riddle_cats: cat_option.set(riddle_cats[0])
        else:
            word_cats = list(CATEGORIES.keys())
            cat_option.configure(values=word_cats)
            if cat_option.get() not in word_cats: cat_option.set(word_cats[0])
    def on_guess_mode_change_with_sound(choice):
        sounds.play_sound("click")
        on_guess_mode_change(choice)
    gm_row = ctk.CTkFrame(frame)
    gm_row.pack(fill="x", pady=4)
    ctk.CTkLabel(gm_row, text="Guessing Mode:").pack(side="left", padx=4)
    gm_option = ctk.CTkOptionMenu(gm_row, values=GUESSING_MODES, command=on_guess_mode_change_with_sound)
    gm_option.set(state.get("guess_mode", "Direct Guess"))
    gm_option.pack(side="left", padx=4)
    on_guess_mode_change(gm_option.get())
    timer_row = ctk.CTkFrame(frame)
    timer_row.pack(fill="x", pady=4)
    ctk.CTkLabel(timer_row, text="Timer:").pack(side="left", padx=4)
    timer_option = ctk.CTkOptionMenu(timer_row, values=list(TIMER_OPTIONS.keys()), command=lambda choice: sounds.play_sound("click"))
    timer_option.set(state.get("timer_label", "No Timer"))
    timer_option.pack(side="left", padx=4)
    btn_row = ctk.CTkFrame(frame)
    btn_row.pack(fill="x", pady=10)
    def read_choices():
        state["username"] = username_entry.get().strip() or "Player"
        state["difficulty"] = diff_option.get()
        state["category"] = cat_option.get()
        state["guess_mode"] = gm_option.get()
        state["timer_label"] = timer_option.get()
        state["timer_seconds"] = TIMER_OPTIONS[state["timer_label"]]
        state["num_words_label"] = num_words_option.get()
        state["num_words_value"] = NUM_WORDS_OPTIONS[state["num_words_label"]]
    ctk.CTkButton(btn_row, text="Start Single Player", command=lambda: (sounds.play_sound("start"), read_choices(), on_start_single())).pack(side="left", expand=True, padx=6)
    ctk.CTkButton(btn_row, text="Start User vs User", command=lambda:  (sounds.play_sound("start"), read_choices(), on_start_uvu())).pack(side="left", expand=True, padx=6)
    ctk.CTkButton(btn_row, text="Start User vs Computer", command=lambda: (sounds.play_sound("start"), read_choices(), on_start_uvc())).pack(side="left", expand=True, padx=6)
    lb_title = ctk.CTkLabel(frame, text="Leaderboard", font=("Consolas", 16, "bold"))
    lb_title.pack(pady=(10, 4))
    lb_box = ctk.CTkTextbox(frame, height=150)
    lb_box.pack(fill="both", expand=True)
    on_refresh(lb_box)
    lb_controls_row = ctk.CTkFrame(frame)
    lb_controls_row.pack(fill="x", pady=(6,0))
    ctk.CTkButton(lb_controls_row, text="Refresh", command=lambda: (sounds.play_sound("click"), on_refresh(lb_box))).pack(side="left", padx=4)
    ctk.CTkButton(lb_controls_row, text="Reset All", command=lambda: (sounds.play_sound('click'), on_reset(lb_box)), fg_color="#D32F2F", hover_color="#B71C1C").pack(side="left", padx=4)
    delete_row = ctk.CTkFrame(frame)
    delete_row.pack(fill="x", pady=6)
    delete_entry = ctk.CTkEntry(delete_row, placeholder_text="Enter name to delete")
    delete_entry.pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(delete_row, text="Delete Player", command=lambda: (sounds.play_sound("click"), on_delete(delete_entry.get(), lb_box))).pack(side="left", padx=4)
    sm_row = ctk.CTkFrame(frame)
    sm_row.pack(fill="x", pady=6)
    ctk.CTkLabel(sm_row, text="Rename Score From:").pack(side="left", padx=4)
    from_entry = ctk.CTkEntry(sm_row, width=120)
    from_entry.pack(side="left", padx=2)
    ctk.CTkLabel(sm_row, text="To:").pack(side="left", padx=4)
    to_entry = ctk.CTkEntry(sm_row, width=120)
    to_entry.pack(side="left", padx=2)
    ctk.CTkButton(sm_row, text="Update Name", command=lambda: (sounds.play_sound("click"), rename_player(from_entry.get().strip(), to_entry.get().strip()), on_refresh(lb_box))).pack(side="left", padx=4)
    return frame

def build_u2u_word_frame(root, state, on_secret_ready):
    frame = ctk.CTkFrame(root)
    ctk.CTkLabel(frame, text="User vs User: Type the secret word, then pass to the guesser.", font=("Consolas", 16, "bold")).pack(pady=8, padx=10)
    row = ctk.CTkFrame(frame)
    row.pack(pady=6)
    ctk.CTkLabel(row, text="Secret Word:").pack(side="left", padx=4)
    entry = ctk.CTkEntry(row, show="*")
    entry.pack(side="left", padx=4)
    status_label = ctk.CTkLabel(frame, text="", text_color="#E57373")
    status_label.pack(pady=(0, 5))
    def on_start_click():
        secret = entry.get().strip()
        if not secret:
            status_label.configure(text="Secret word cannot be empty.")
            return
        state["secret_word"] = secret
        on_secret_ready()
    ctk.CTkButton(frame, text="Start Guessing", command=on_start_click).pack(pady=8)
    return frame

def build_game_frame_single(root, state, on_back, on_guess, on_hint, on_quit, on_next_or_replay, session_state):
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    top = ctk.CTkFrame(frame)
    top.pack(fill="x")
    ctk.CTkButton(top, text="Back", command=lambda: (sounds.play_sound("click"), on_back()), width=80).pack(side="left", padx=4)
    word_count_label = ctk.CTkLabel(top, text="")
    word_count_label.pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Player: {state['username']}").pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Difficulty: {state['difficulty']}").pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Mode: {state['guess_mode']}").pack(side="left", padx=6)
    category_label = ctk.CTkLabel(top, text=f"Category: {state['category']}")
    category_label.pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Score: {get_player_score(state['username'])}").pack(side="right", padx=6)

    mid = ctk.CTkFrame(frame)
    mid.pack(fill="both", pady=8, expand=True)
    art_label = ctk.CTkLabel(mid, text="", font=("Consolas", 12), justify="left")
    art_label.pack(side="left", padx=6, anchor="n")
    right = ctk.CTkFrame(mid)
    right.pack(side="left", padx=10, fill="both", expand=True)
    main_question_label = ctk.CTkLabel(right, text="", font=("Consolas", 16, "italic"), wraplength=400, justify="center")
    main_question_label.pack(pady=(5, 10))
    word_label = ctk.CTkLabel(right, text="", font=("Consolas", 32, "bold"))
    word_label.pack(pady=(10, 6))
    guessed_label = ctk.CTkLabel(right, text="Guessed: ", font=("Consolas", 12))
    guessed_label.pack(pady=(0, 6))
    lives_label = ctk.CTkLabel(right, text="Lives left: ")
    lives_label.pack(pady=(0, 10))
    ctk.CTkLabel(right, text="Type a letter to make a guess.", font=("Consolas", 14)).pack(pady=6)
    hint_row = ctk.CTkFrame(right)
    hint_row.pack(pady=4)
    hints_label = ctk.CTkLabel(hint_row, text="Hints left: ")
    hints_label.pack(side="left", padx=4)
    ctk.CTkButton(hint_row, text="Use Hint", command=on_hint).pack(side="left", padx=4)
    timer_label = ctk.CTkLabel(right, text="")
    timer_label.pack(anchor="w", pady=4)

    bottom = ctk.CTkFrame(frame)
    bottom.pack(fill="x", pady=8, side="bottom")
    status_label = ctk.CTkLabel(bottom, text="Ready.")
    status_label.pack(side="left", padx=4, expand=True, anchor="w")
    
    next_word_button = ctk.CTkButton(bottom, text="Next Word", command=lambda: (sounds.play_sound("click"), on_next_or_replay()))
    next_word_button.pack(side="right", padx=4)
    ctk.CTkButton(bottom, text="Quit Game", command=lambda: (sounds.play_sound("click"), on_quit())).pack(side="right", padx=4)

    return frame, {
        "art_label": art_label, "word_label": word_label, "guessed_label": guessed_label,
        "hints_label": hints_label, "lives_label": lives_label,
        "timer_label": timer_label, "status_label": status_label,
        "main_question_label": main_question_label,
        "category_label": category_label,
        "word_count_label": word_count_label,
        "next_word_button": next_word_button
    }

def build_game_frame_uvc(root, state, on_back, on_user_guess, on_hint, on_quit, on_next_or_replay, session_state):
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    top = ctk.CTkFrame(frame)
    top.pack(fill="x")
    ctk.CTkButton(top, text="Back", command=lambda: (sounds.play_sound("click"), on_back()), width=80).pack(side="left", padx=4)
    word_count_label = ctk.CTkLabel(top, text="")
    word_count_label.pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Player: {state['username']}").pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Difficulty: {state['difficulty']}").pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Mode: {state['guess_mode']}").pack(side="left", padx=6)
    category_label = ctk.CTkLabel(top, text=f"Category: {state['category']}")
    category_label.pack(side="left", padx=6)
    ctk.CTkLabel(top, text=f"Score: {get_player_score(state['username'])}").pack(side="right", padx=6)

    main_question_label = ctk.CTkLabel(frame, text="", font=("Consolas", 16, "italic"), wraplength=600, justify="center")
    main_question_label.pack(pady=(5, 10), fill="x")
    boards = ctk.CTkFrame(frame)
    boards.pack(fill="both", pady=8, expand=True)
    left_board = ctk.CTkFrame(boards)
    left_board.pack(side="left", padx=6, expand=True, fill="both")
    right_board = ctk.CTkFrame(boards)
    right_board.pack(side="left", padx=6, expand=True, fill="both")
    ctk.CTkLabel(left_board, text="Your Board", font=("Consolas", 14, "bold")).pack()
    user_art = ctk.CTkLabel(left_board, text="", font=("Consolas", 12), justify="left")
    user_art.pack()
    user_word = ctk.CTkLabel(left_board, text="", font=("Consolas", 22, "bold"))
    user_word.pack()
    user_guessed = ctk.CTkLabel(left_board, text="Guessed: ", font=("Consolas", 12))
    user_guessed.pack()
    user_lives = ctk.CTkLabel(left_board, text="Lives left: ")
    user_lives.pack()
    ctk.CTkLabel(right_board, text="Computer Board", font=("Consolas", 14, "bold")).pack()
    comp_art = ctk.CTkLabel(right_board, text="", font=("Consolas", 12), justify="left")
    comp_art.pack()
    comp_word = ctk.CTkLabel(right_board, text="", font=("Consolas", 22, "bold"))
    comp_word.pack()
    comp_guessed = ctk.CTkLabel(right_board, text="Guessed: ", font=("Consolas", 12))
    comp_guessed.pack()
    comp_lives = ctk.CTkLabel(right_board, text="Lives left: ")
    comp_lives.pack()
    control_frame = ctk.CTkFrame(frame)
    control_frame.pack(fill="x", side="bottom", pady=4)
    ctk.CTkLabel(control_frame, text="Type a letter to make your guess.", font=("Consolas", 14)).pack(pady=4)
    hint_row = ctk.CTkFrame(control_frame)
    hint_row.pack(pady=4)
    hints_label = ctk.CTkLabel(hint_row, text=f"Hints left: {state['user']['hints_left']}")
    hints_label.pack(side="left", padx=4)
    ctk.CTkButton(hint_row, text="Use Hint", command=on_hint).pack(side="left", padx=4)

    status_frame = ctk.CTkFrame(control_frame)
    status_frame.pack(fill="x", pady=4)
    timer_label = ctk.CTkLabel(status_frame, text="")
    timer_label.pack(side="left", padx=4)
    status_label = ctk.CTkLabel(status_frame, text="User starts.")
    status_label.pack(side="left", padx=4, expand=True, anchor="w")
    
    next_word_button = ctk.CTkButton(status_frame, text="Next Word", command=lambda: (sounds.play_sound("click"), on_next_or_replay()))
    next_word_button.pack(side="right", padx=4)
    ctk.CTkButton(status_frame, text="Quit Game", command=lambda: (sounds.play_sound("click"), on_quit())).pack(side="right", padx=4)

    return frame, {
        "user_art": user_art, "user_word": user_word, "user_guessed": user_guessed, "user_lives": user_lives,
        "comp_art": comp_art, "comp_word": comp_word, "comp_guessed": comp_guessed, "comp_lives": comp_lives,
        "hints_label": hints_label, "timer_label": timer_label, "status_label": status_label,
        "main_question_label": main_question_label,
        "category_label": category_label,
        "word_count_label": word_count_label,
        "next_word_button": next_word_button
    }