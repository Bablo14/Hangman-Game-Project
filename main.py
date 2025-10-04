import customtkinter as ctk
from config import DIFFICULTIES, NUM_WORDS_OPTIONS, POINTS_USE_HINT
from ui_components import (
    build_start_frame, build_u2u_word_frame,
    build_game_frame_single, build_game_frame_uvc
)
from game_logic import (
    init_single_state, init_user_vs_user_state, init_user_vs_computer_state,
    apply_letter_guess, use_hint_on, is_win, is_loss,
    finalize_score, computer_pick_letter, mask_word, mask_computer_display
)
from scores import leaderboard, reset_leaderboard, delete_player_score
from hangman_art import map_progress_to_art
from timers import start_timer, cancel_timer
import sounds

STATE = {
    "username": "", "difficulty": "Easy", "category": "Animals",
    "guess_mode": "Direct Guess", "timer_label": "No Timer", "timer_seconds": 0,
    "secret_word": "", "num_words_label": "Unlimited", "num_words_value": float('inf'),
}

def main():
    sounds.init_sound()
    sounds.play_sound("open")
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.title("Hangman Guessing Game")
    app.geometry("900x700")

    current_frame = {"ref": None}
    timer_ctrl = {"ref": None}

    def show_frame(new_frame):
        if current_frame["ref"] is not None: current_frame["ref"].pack_forget()
        current_frame["ref"] = new_frame
        new_frame.pack(fill="both", expand=True)

    def go_start():
        def refresh_leaderboard_display(textbox):
            textbox.configure(state="normal")
            textbox.delete("1.0", "end")
            rows = leaderboard()
            textbox.insert("end", f"{'Rank':<6}   {'Player':<20}    {'Score':>8}\n")
            textbox.insert("end", "-"*60 + "\n")
            if not rows: textbox.insert("end", "\n" + " " * 15 + "No scores yet!")
            else:
                for i, (name, score) in enumerate(rows, start=1):
                    textbox.insert("end", f"{i:<6}      {name:<20}     {score:>8}\n")
            textbox.configure(state="disabled")
        def do_reset_leaderboard(textbox):
            reset_leaderboard()
            refresh_leaderboard_display(textbox)
        def do_delete_player(username, textbox):
            if username:
                delete_player_score(username)
                refresh_leaderboard_display(textbox)
        frame = build_start_frame(
            app, STATE, on_start_single=start_single_player_session, on_start_uvu=go_u2u_secret,
            on_start_uvc=start_uvc_session, on_refresh=refresh_leaderboard_display,
            on_reset=do_reset_leaderboard, on_delete=do_delete_player
        )
        show_frame(frame)

    def start_single_player_session():
        session_state = {'used_words': set(), 'words_played': 0}
        run_next_word_single(session_state)

    def start_uvc_session():
        session_state = {'used_words': set(), 'words_played': 0}
        run_next_word_uvc(session_state)
    
    def go_u2u_secret():
        frame = build_u2u_word_frame(app, STATE, on_secret_ready=go_u2u_configured)
        show_frame(frame)
        
    def go_u2u_configured():
        secret = STATE.get("secret_word", "").strip()
        g = init_user_vs_user_state(STATE["username"], STATE["difficulty"], secret)
        build_single_game(g, None)

    def start_turn_timer(seconds, on_timeup, set_label):
        if timer_ctrl["ref"]: cancel_timer(app, timer_ctrl["ref"])
        timer_ctrl["ref"] = None
        if seconds <= 0:
            set_label("Timer: OFF")
            return
        def on_tick(rem): set_label(f"Timer: {rem}s")
        timer_ctrl["ref"] = start_timer(app, seconds, on_tick, on_timeup)
    def stop_turn_timer():
        if timer_ctrl["ref"]: cancel_timer(app, timer_ctrl["ref"])
        timer_ctrl["ref"] = None

    def run_next_word_single(session_state):
        gstate = init_single_state(STATE["username"], STATE["difficulty"], STATE["category"], STATE["guess_mode"], session_state['used_words'])
        build_single_game(gstate, session_state)
        
    def run_next_word_uvc(session_state):
        gstate = init_user_vs_computer_state(STATE["username"], STATE["difficulty"], STATE["category"], STATE["guess_mode"], session_state['used_words'])
        build_uvc_game(gstate, session_state)

    def build_single_game(gstate, session_state):
        is_session = session_state is not None

        def on_next_or_replay():
            if not is_session:
                go_u2u_secret()
                return
            stop_turn_timer()
            app.bind("<Key>", lambda e: None)
            session_state['used_words'].add(gstate['word'])
            session_state['words_played'] += 1
            if session_state['words_played'] < STATE['num_words_value']:
                run_next_word_single(session_state)
            else:
                start_single_player_session()

        def on_back():
            stop_turn_timer()
            app.bind("<Key>", lambda e: None)
            go_start()

        def update_ui():
            refs["art_label"].configure(text=map_progress_to_art(gstate["max_lives"], gstate["lives_left"]))
            refs["word_label"].configure(text=gstate["display"])
            refs["guessed_label"].configure(text=f"Guessed: {', '.join(sorted(gstate['guessed']))}")
            refs["hints_label"].configure(text=f"Hints left: {gstate['hints_left']}")
            refs["lives_label"].configure(text=f"Lives left: {gstate['lives_left']}")
            if gstate.get("question_text"):
                refs["main_question_label"].configure(text=gstate["question_text"])
            if is_session:
                limit = STATE['num_words_value']
                if limit == float('inf'):
                    refs["word_count_label"].configure(text=f"Word: {session_state['words_played'] + 1}")
                else:
                    refs["word_count_label"].configure(text=f"Word: {session_state['words_played'] + 1} of {int(limit)}")
        
        def post_turn_check():
            game_over = is_win(gstate["display"]) or is_loss(gstate["lives_left"])
            if game_over:
                refs['next_word_button'].configure(state="normal")
                stop_turn_timer()
                app.bind("<Return>", lambda e: (sounds.play_sound("click"), on_next_or_replay()))
                if is_session and (session_state['words_played'] + 1) >= STATE['num_words_value']:
                    refs['next_word_button'].configure(text="Replay")
                if is_win(gstate["display"]):
                    sounds.play_sound("win")
                    final, total = finalize_score(gstate["username"], gstate["score_delta"], gstate["multiplier"], True)
                    refs["status_label"].configure(text=f"You win! +{final} pts. Total: {total}")
                else: # This is a loss from running out of lives
                    sounds.play_sound("loss")
                    finalize_score(gstate["username"], gstate["score_delta"], gstate["multiplier"], False)
                    refs["status_label"].configure(text=f"You lost. The word was: {gstate['word']}")
        
        def do_guess(ch):
            if is_win(gstate["display"]) or is_loss(gstate["lives_left"]): return
            ch = (ch or "").strip().lower()
            status, gstate["guessed"], gstate["lives_left"], delta = apply_letter_guess(gstate["word"], gstate["guessed"], gstate["lives_left"], ch)
            
            if status == 'already_guessed':
                refs["status_label"].configure(text="You've already guessed. Try another.")
                return

            if status == 'correct':
                sounds.play_sound("correct")
                refs["status_label"].configure(text="Good guess!")
                gstate["correct_streak"] += 1
            elif status == 'wrong':
                sounds.play_sound("wrong")
                refs["status_label"].configure(text="Wrong letter.")
                gstate["correct_streak"] = 0
            
            if status in ('correct', 'wrong'):
                gstate["display"] = mask_word(gstate["word"], gstate["guessed"])
                gstate["score_delta"] += delta
                update_ui()

                # NEW: Check for streak and reset timer
                if gstate.get("correct_streak", 0) >= 3:
                    sounds.play_sound("win") # Or a special "streak" sound
                    refs["status_label"].configure(text="3 in a row! Timer reset.")
                    gstate["correct_streak"] = 0
                    if STATE["timer_seconds"] > 0:
                        start_turn_timer(STATE["timer_seconds"], on_time_expired, lambda t: refs["timer_label"].configure(text=t))
                
                post_turn_check()

        def do_hint():
            if is_win(gstate["display"]) or is_loss(gstate["lives_left"]): return
            gstate["correct_streak"] = 0 # Using a hint breaks the streak
            hints_before = gstate["hints_left"]
            round_score_before = gstate["score_delta"]
            new_disp, gstate["guessed"], gstate["hints_left"], delta = use_hint_on(gstate["word"], gstate["display"], gstate["guessed"], gstate["hints_left"])
            if gstate["hints_left"] < hints_before:
                sounds.play_sound("hint")
                gstate["score_delta"] += delta
                hints_used = gstate['max_hints'] - gstate['hints_left']
                round_score_after = gstate["score_delta"]
                message = f"Hint {hints_used} used: Round score {round_score_before} + ({delta}) = {round_score_after}"
                refs["status_label"].configure(text=message)
            else:
                refs["status_label"].configure(text="No hints available or no letters to reveal.")
            gstate["display"] = new_disp
            update_ui()
            post_turn_check()

        def on_time_expired():
            # NEW: Time's up automatically ends the word and moves on
            stop_turn_timer()
            app.bind("<Key>", lambda e: None)
            app.bind("<Return>", lambda e: None)
            sounds.play_sound("loss")
            finalize_score(gstate["username"], gstate["score_delta"], gstate["multiplier"], False)
            refs["status_label"].configure(text=f"Time's Up! The word was: {gstate['word']}")
            # Automatically move to the next word after a 2-second delay
            app.after(2000, on_next_or_replay)

        frame, refs = build_game_frame_single(
            app, gstate, on_back=on_back, on_guess=do_guess, on_hint=do_hint,
            on_quit=on_back, on_next_or_replay=on_next_or_replay, session_state=session_state
        )
        if not is_session: refs["next_word_button"].configure(text="Replay")
        refs['next_word_button'].configure(state="disabled")
        show_frame(frame)
        app.bind("<Return>", lambda e: None) 
        app.bind("<Key>", lambda e: do_guess(e.char) if e.char.isalpha() else None)
        start_turn_timer(STATE["timer_seconds"], on_time_expired, lambda t: refs["timer_label"].configure(text=t))
        update_ui()

    def build_uvc_game(gstate, session_state):
        user_finished, computer_finished = False, False
        
        def on_next_or_replay():
            stop_turn_timer()
            app.bind("<Key>", lambda e: None)
            session_state['used_words'].add(gstate['word'])
            session_state['words_played'] += 1
            if session_state['words_played'] < STATE['num_words_value']:
                run_next_word_uvc(session_state)
            else:
                start_uvc_session()

        def on_back():
            stop_turn_timer()
            app.bind("<Key>", lambda e: None)
            go_start()
            
        def update_ui():
            is_game_over = user_finished and computer_finished
            refs["user_art"].configure(text=map_progress_to_art(gstate["max_lives"], gstate["user"]["lives_left"]))
            refs["user_word"].configure(text=gstate["user"]["display"])
            refs["user_guessed"].configure(text=f"Guessed: {', '.join(sorted(gstate['user']['guessed']))}")
            refs["user_lives"].configure(text=f"Lives left: {gstate['user']['lives_left']}")
            refs["comp_art"].configure(text=map_progress_to_art(gstate["max_lives"], gstate["computer"]["lives_left"]))
            refs["comp_word"].configure(text=gstate["computer"]["display"])
            refs["comp_lives"].configure(text=f"Lives left: {gstate['computer']['lives_left']}")
            if is_game_over: comp_guessed_display = f"Guessed: {', '.join(sorted(gstate['computer']['guessed']))}"
            else: comp_guessed_display = f"Guessed: {' '.join(['*' for _ in gstate['computer']['guessed']])}"
            refs["comp_guessed"].configure(text=comp_guessed_display)
            if gstate.get("question_text"): refs["main_question_label"].configure(text=gstate["question_text"])
            limit = STATE['num_words_value']
            if limit == float('inf'):
                refs["word_count_label"].configure(text=f"Word: {session_state['words_played'] + 1}")
            else:
                refs["word_count_label"].configure(text=f"Word: {session_state['words_played'] + 1} of {int(limit)}")
            if is_game_over:
                if is_win(gstate["user"]["display"]):
                    refs["user_word"].configure(text=' '.join(list(gstate['word'])))
                refs["comp_word"].configure(text=mask_word(gstate["word"], gstate["computer"]["guessed"]))

        def resolve_game():
            nonlocal user_finished, computer_finished
            user_finished, computer_finished = True, True
            refs['next_word_button'].configure(state="normal")
            stop_turn_timer()
            app.bind("<Return>", lambda e: (sounds.play_sound("click"), on_next_or_replay()))
            if (session_state['words_played'] + 1) >= STATE['num_words_value']:
                refs['next_word_button'].configure(text="Replay")
            user_won = is_win(gstate["user"]["display"])
            comp_won = is_win(gstate["computer"]["display"])
            did_win_for_score = user_won and not comp_won
            base = gstate["user"].get("score_delta", 0)
            final, total = finalize_score(gstate["username"], base, gstate["multiplier"], did_win_for_score)
            if user_won and not comp_won: message = f"User wins with {gstate['user']['lives_left']} lives left! +{final} pts."; sounds.play_sound("win")
            elif comp_won and not user_won: message = f"Computer wins. The word was: {gstate['word']}. {final} pts."; sounds.play_sound("loss")
            else: message = f"It's a draw! The word was: {gstate['word']}. {final} pts."; sounds.play_sound("draw")
            refs["status_label"].configure(text=f"{message} Total: {total}")
            update_ui()
            
        def run_computer_simulation():
            nonlocal computer_finished
            refs["status_label"].configure(text="You've finished! Simulating computer's remaining turns...")
            while not computer_finished:
                if is_win(gstate["computer"]["display"]) or is_loss(gstate["computer"]["lives_left"]): computer_finished = True; continue
                ch = computer_pick_letter(gstate)
                _, gstate["computer"]["guessed"], gstate["computer"]["lives_left"], _ = apply_letter_guess(gstate["word"], gstate["computer"]["guessed"], gstate["computer"]["lives_left"], ch or "")
                gstate["computer"]["display"] = mask_computer_display(gstate["word"], gstate["computer"]["guessed"])
            update_ui()
            resolve_game()

        def check_completion_and_continue(player_who_just_moved):
            nonlocal user_finished, computer_finished
            if not user_finished and (is_win(gstate["user"]["display"]) or is_loss(gstate["user"]["lives_left"])): user_finished = True
            if not computer_finished and (is_win(gstate["computer"]["display"]) or is_loss(gstate["computer"]["lives_left"])): computer_finished = True
            if user_finished and computer_finished: resolve_game(); return
            if player_who_just_moved == "user":
                if user_finished and not computer_finished: run_computer_simulation()
                elif not computer_finished: start_computer_turn()
            elif player_who_just_moved == "computer" and not user_finished: start_user_turn()

        def start_computer_turn():
            gstate["turn"] = "computer"; refs["status_label"].configure(text="Computer thinking..."); app.after(1000, on_time_comp)

        def on_time_comp():
            if computer_finished or gstate["turn"] != "computer": return
            ch = computer_pick_letter(gstate)
            _, gstate["computer"]["guessed"], gstate["computer"]["lives_left"], _ = apply_letter_guess(gstate["word"], gstate["computer"]["guessed"], gstate["computer"]["lives_left"], ch or "")
            gstate["computer"]["display"] = mask_computer_display(gstate["word"], gstate["computer"]["guessed"])
            update_ui()
            check_completion_and_continue("computer")

        def start_user_turn():
            gstate["turn"] = "user"; refs["status_label"].configure(text="Your turn."); start_turn_timer(STATE["timer_seconds"], on_time_user, set_timer_text)

        def on_time_user():
            # NEW: Time's up in UVC mode automatically ends the round
            stop_turn_timer()
            app.bind("<Key>", lambda e: None)
            app.bind("<Return>", lambda e: None)
            sounds.play_sound("loss")
            finalize_score(gstate["username"], gstate["user"].get("score_delta", 0), gstate["multiplier"], False)
            refs["status_label"].configure(text=f"Time's Up! The word was: {gstate['word']}")
            app.after(2000, on_next_or_replay)
        
        def do_user_guess(ch):
            if user_finished or gstate["turn"] != "user": return
            ch = (ch or "").strip().lower()
            status, gstate["user"]["guessed"], gstate["user"]["lives_left"], delta = apply_letter_guess(gstate["word"], gstate["user"]["guessed"], gstate["user"]["lives_left"], ch)
            if status == 'already_guessed': refs["status_label"].configure(text="You've already guessed. Try another."); return
            
            if status == 'correct':
                sounds.play_sound("correct")
                gstate["user"]["correct_streak"] += 1
            elif status == 'wrong':
                sounds.play_sound("wrong")
                gstate["user"]["correct_streak"] = 0

            if status in ('correct', 'wrong'):
                gstate["user"]["score_delta"] = gstate["user"].get("score_delta", 0) + delta
                gstate["user"]["display"] = mask_word(gstate["word"], gstate["user"]["guessed"])
                update_ui()

                if gstate["user"].get("correct_streak", 0) >= 3:
                    sounds.play_sound("win")
                    refs["status_label"].configure(text="3 in a row! Timer reset.")
                    gstate["user"]["correct_streak"] = 0
                    if STATE["timer_seconds"] > 0:
                        start_turn_timer(STATE["timer_seconds"], on_time_user, set_timer_text)

                stop_turn_timer()
                check_completion_and_continue("user")

        def do_hint():
            if user_finished or gstate["turn"] != "user": return
            gstate["user"]["correct_streak"] = 0 # Using a hint breaks the streak
            if gstate["user"]["hints_left"] <= 0:
                refs["status_label"].configure(text="No hints available. Guess a letter.")
                sounds.play_sound("wrong")
                return
            hints_before = gstate["user"]["hints_left"]
            round_score_before = gstate["user"].get("score_delta", 0)
            new_disp, guessed, hints_left, delta = use_hint_on(gstate["word"], gstate["user"]["display"], gstate["user"]["guessed"], gstate["user"]["hints_left"])
            if hints_left < hints_before:
                sounds.play_sound("hint")
                gstate["user"]["score_delta"] = round_score_before + delta
                hints_used = gstate['user']['max_hints'] - hints_left
                round_score_after = gstate["user"]["score_delta"]
                message = f"Hint {hints_used} used: Round score {round_score_before} + ({delta}) = {round_score_after}"
                refs["status_label"].configure(text=message)
            gstate["user"]["display"] = new_disp
            gstate["user"]["guessed"] = guessed
            gstate["user"]["hints_left"] = hints_left
            refs["hints_label"].configure(text=f"Hints left: {gstate['user']['hints_left']}")
            update_ui()
            stop_turn_timer()
            check_completion_and_continue("user")

        def set_timer_text(t): refs["timer_label"].configure(text=t)
        frame, refs = build_game_frame_uvc(
            app, gstate, on_back=on_back, on_user_guess=do_user_guess, on_hint=do_hint,
            on_quit=on_back, on_next_or_replay=on_next_or_replay, session_state=session_state
        )
        refs['next_word_button'].configure(state="disabled")
        show_frame(frame)
        app.bind("<Return>", lambda e: None)
        app.bind("<Key>", lambda e: do_user_guess(e.char) if e.char.isalpha() else None)
        start_user_turn()
        update_ui()

    go_start()
    app.mainloop()

if __name__ == "__main__":
    main()