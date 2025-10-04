# sounds.py
import pygame
import os
import sys

SOUNDS = {}

def init_sound():
    """Initializes the pygame mixer and pre-loads all sound files."""
    try:
        pygame.mixer.init()
        sound_files = {
            # Game Events
            "open": os.path.join("sound", "open.wav"), # NEW opening sound
            "correct": os.path.join("sound", "correct.wav"),
            "wrong": os.path.join("sound", "wrong.wav"),
            "win": os.path.join("sound", "win.wav"),
            "loss": os.path.join("sound", "loss.wav"),
            "draw": os.path.join("sound", "draw.wav"),
            "hint": os.path.join("sound", "hint.wav"),
            "time_up": os.path.join("sound", "time_up.wav"),

            # UI Sounds
            "click": os.path.join("sound", "click.wav"),
            "start": os.path.join("sound", "start.wav"),
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                SOUNDS[name] = pygame.mixer.Sound(path)
            else:
                print(f"Warning: Sound file not found at {path}")

    except Exception as e:
        print(f"Error initializing sound system: {e}")
        pygame.mixer.quit()

def play_sound(name):
    """Plays a pre-loaded sound by its name."""
    if name in SOUNDS:
        try:
            SOUNDS[name].play()
        except Exception as e:
            print(f"Error playing sound '{name}': {e}")