# hangman_art.py
# ASCII hangman stages as strings, displayed in Labels (no Canvas).

# 8-step art (for Easy); for fewer lives, we'll map progress proportionally.
HANGMAN_8 = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """,
    """
     +---+
     |   |
    [O]  |
    /|\  |
    / \  |
         |
    =========
    """,
]

def map_progress_to_art(max_lives, lives_left):
    # Convert current life state to stage index
    # For 8 lives we use HANGMAN_8 directly; for 6/4 we scale into 0..7
    if max_lives <= 0:
        idx = 7
    else:
        used = max_lives - lives_left
        scale = 7 / max(1, max_lives - 1)
        idx = int(round(used * scale))
    return HANGMAN_8[min(max(idx, 0), 7)]
