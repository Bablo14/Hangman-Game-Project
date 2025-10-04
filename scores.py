# scores.py
import json

SCORE_FILE = "scores.json"
SCORES = {}

def load_scores():
    """Load scores from the JSON file into memory."""
    global SCORES
    try:
        with open(SCORE_FILE, "r") as f:
            SCORES = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        SCORES = {}

def save_scores():
    """Save the current scores from memory to the JSON file."""
    with open(SCORE_FILE, "w") as f:
        json.dump(SCORES, f, indent=4)

def get_player_score(username):
    """Get the score for a specific player."""
    return SCORES.get(username, 0)

def set_player_score(username, score):
    """Set the score for a specific player and save."""
    SCORES[username] = score
    save_scores()

def reset_player_score(username):
    """Reset a single player's score to zero."""
    if username in SCORES:
        SCORES[username] = 0
        save_scores()

def delete_player_score(username):
    """Deletes a player's score record entirely."""
    if SCORES.pop(username, None) is not None:
        save_scores()

def rename_player(old_name, new_name):
    """Rename a player in the leaderboard if the old name exists."""
    if old_name in SCORES and new_name and old_name != new_name:
        SCORES[new_name] = SCORES.pop(old_name)
        save_scores()

def leaderboard():
    """Return a sorted list of (name, score) tuples for the top 10 players."""
    return sorted(SCORES.items(), key=lambda item: item[1], reverse=True)[:10]

def reset_leaderboard():
    """Clear all scores and save the empty leaderboard."""
    global SCORES
    SCORES = {}
    save_scores()

# Load scores when the module is first imported
load_scores()