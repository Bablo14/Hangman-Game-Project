# # config.py
# # Centralized configuration and constants for the Hangman project.

# # Difficulty setup: lives and score multipliers
# DIFFICULTIES = {
#     "Easy": {"lives": 8, "multiplier": 1.0, "hints": 2},     # 8 lives, 2 hints, 1x [design]
#     "Medium": {"lives": 6, "multiplier": 1.5, "hints": 3},   # 6 lives, 3 hints, 1.5x [design]
#     "Hard": {"lives": 4, "multiplier": 2.0, "hints": 4},     # 4 lives, 4 hints (as requested), 2x [design]
# }

# # Timer options in seconds
# TIMER_OPTIONS = {
#     "No Timer": 0,
#     "15 sec": 15,
#     "30 sec": 30,
#     "60 sec": 60,
# }



# # Player modes
# PLAYER_MODES = [
#     "Single Player",
#     "User vs User",
#     "User vs Computer",
# ]

# # Guessing modes
# GUESSING_MODES = [
#     "Direct Guess",
#     "Question-Based",
# ]

# # Score penalties and rewards (basic defaults; can be tuned)
# POINTS_CORRECT_LETTER = 10
# POINTS_WRONG_LETTER = -5
# POINTS_USE_HINT = -7   # using a hint reduces score
# POINTS_WIN_BONUS = 25
# POINTS_LOSS_PENALTY = -10

# # Leaderboard size
# LEADERBOARD_LIMIT = 10

# # Misc labels/text
# APP_TITLE = "Hangman Guessing Game"
# LOGO_TEXT = r"""
#  _   _                                          
# | | | | __ _ _ __   __ _ _ __ ___   __ _ _ __  
# | |_| |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
# |  _  | (_| | | | | (_| | | | | | | (_| | | | |
# |_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
#                    |___/                       
# """


"""Update Version"""
# config.py

# Number of words to play in a session
NUM_WORDS_OPTIONS = {
    "5 Words": 5,
    "10 Words": 10,
    "20 Words": 20,
    "Unlimited": float('inf'), # Use infinity to represent unlimited
}

DIFFICULTIES = {
    "Easy": {"lives": 8, "multiplier": 1.0, "hints": 2},
    "Medium": {"lives": 6, "multiplier": 1.5, "hints": 3},
    "Hard": {"lives": 4, "multiplier": 2.0, "hints": 4},
}

# Timer options in seconds
TIMER_OPTIONS = {
    "No Timer": 0,
    "15 sec": 15,
    "30 sec": 30,
    "60 sec": 60,
}

# Player modes
PLAYER_MODES = [
    "Single Player",
    "User vs User",
    "User vs Computer",
]

# Guessing modes
GUESSING_MODES = [
    "Direct Guess",
    "Question-Based",
]

# Score penalties and rewards
POINTS_CORRECT_LETTER = 10
POINTS_WRONG_LETTER = -5
POINTS_USE_HINT = -7
POINTS_WIN_BONUS = 25
POINTS_LOSS_PENALTY = -10

# Leaderboard size
LEADERBOARD_LIMIT = 10

# Misc labels/text
APP_TITLE = "Hangman Guessing Game"
LOGO_TEXT = r"""
 _   _
| | | | __ _ _ __   __ _ _ __ ___   __ _ _ __
| |_| |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
|  _  | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                  |___/
"""