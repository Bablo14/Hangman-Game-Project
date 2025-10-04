# # # questions.py
# # # Question-based guessing: present a tricky question with a masked answer.
# # # Player guesses ONE letter for the masked answer; if it appears, they can use that same letter as a guess on the hangman word.

# import os
# import json
# import random
# from collections import Counter

# QUESTIONS = [
#     {"q": "It has keys but no locks; it has space but no room; you can enter but can't go outside. What is it?", "answer": "keyboard"},
#     {"q": "What can travel around the world while staying in a corner?", "answer": "stamp"},
#     {"q": "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?", "answer": "echo"},
#     {"q": "I’m tall when I’m young, and I’m short when I’m old. What am I?", "answer": "candle"},

#     # ✅ New 50 tricky riddles
#     {"q": "What has to be broken before you can use it?", "answer": "egg"},
#     {"q": "What has hands but can’t clap?", "answer": "clock"},
#     {"q": "What has a head, a tail, but no body?", "answer": "coin"},
#     {"q": "What gets wetter as it dries?", "answer": "towel"},
#     {"q": "What has many teeth but cannot bite?", "answer": "comb"},
#     {"q": "What has one eye but cannot see?", "answer": "needle"},
#     {"q": "The more of me you take, the more you leave behind. What am I?", "answer": "footsteps"},
#     {"q": "What comes down but never goes up?", "answer": "rain"},
#     {"q": "What has legs but doesn’t walk?", "answer": "table"},
#     {"q": "What can you catch but not throw?", "answer": "cold"},
#     {"q": "What belongs to you but other people use it more?", "answer": "name"},
#     {"q": "What has cities but no houses, forests but no trees, and rivers but no water?", "answer": "map"},
#     {"q": "The more you take away from me, the bigger I get. What am I?", "answer": "hole"},
#     {"q": "What has an endless supply of letters but starts empty?", "answer": "mailbox"},
#     {"q": "What has an ear but cannot hear?", "answer": "corn"},
#     {"q": "What is full of holes but still holds water?", "answer": "sponge"},
#     {"q": "I’m always running, but I never move. What am I?", "answer": "time"},
#     {"q": "What has four fingers and a thumb but is not alive?", "answer": "glove"},
#     {"q": "What has a neck but no head?", "answer": "bottle"},
#     {"q": "What gets sharper the more you use it?", "answer": "brain"},
#     {"q": "The more you share me, the less I become. What am I?", "answer": "secret"},
#     {"q": "What has a bed but never sleeps?", "answer": "river"},
#     {"q": "What can fill a room but takes up no space?", "answer": "light"},
#     {"q": "What has wings but cannot fly?", "answer": "pen"},
#     {"q": "What has roots that nobody sees and is taller than trees?", "answer": "mountain"},
#     {"q": "What has words but never speaks?", "answer": "book"},
#     {"q": "I’m always in front of you but can’t be seen. What am I?", "answer": "future"},
#     {"q": "The more you take from me, the more I leave behind. What am I?", "answer": "memories"},
#     {"q": "What goes up but never comes down?", "answer": "age"},
#     {"q": "What runs but has no legs?", "answer": "water"},
#     {"q": "What has a face and two hands but no arms or legs?", "answer": "clock"},
#     {"q": "What flies without wings?", "answer": "time"},
#     {"q": "What has an end but no beginning?", "answer": "stick"},
#     {"q": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "letter m"},
#     {"q": "What is always moving but never arrives?", "answer": "horizon"},
#     {"q": "What has 88 keys but cannot open a door?", "answer": "piano"},
#     {"q": "What can be cracked, made, told, and played?", "answer": "joke"},
#     {"q": "I’m lighter than a feather, yet the strongest person can’t hold me for long. What am I?", "answer": "breath"},
#     {"q": "What has a ring but no finger?", "answer": "telephone"},
#     {"q": "What has a tongue but cannot talk?", "answer": "shoe"},
#     {"q": "What is always hungry and must be fed, but dies if given water?", "answer": "fire"},
#     {"q": "What can you break, even if you never touch it?", "answer": "promise"},
#     {"q": "What has one head, one foot, and four legs?", "answer": "bed"},
#     {"q": "What has branches but no leaves or fruit?", "answer": "bank"},
#     {"q": "What runs but never walks, murmurs but never talks?", "answer": "river"},
#     {"q": "What has a spine but no bones?", "answer": "book"},
#     {"q": "What has a heart but no other organs?", "answer": "deck of cards"},
#     {"q": "What has a bottom at the top?", "answer": "leg"},
#     {"q": "What is so fragile that saying its name breaks it?", "answer": "silence"},
#     {"q": "What has an eye but cannot blink?", "answer": "hurricane"},
#     {"q": "What has many rings but no fingers?", "answer": "tree"},
#     {"q": "What is always in front of you but you can’t see?", "answer": "future"},
    
#     # ✅ New 50 Pokémon-themed riddles
    
#     {"q": "I have red cheeks and thunder in my tail. Who am I?", "answer": "pikachu"},
#     {"q": "I carry a giant leek and never go hungry. Who am I?", "answer": "farfetchd"},
#     {"q": "I’m known as the Flame Pokémon starter from Kanto. Who am I?", "answer": "charmander"},
#     {"q": "I evolve with a Thunder Stone and become much stronger. Who am I?", "answer": "pikachu"},
#     {"q": "I look like a rock but explode when touched. Who am I?", "answer": "voltorb"},
#     {"q": "I’m a fish that evolves into a mighty dragon-like beast. Who am I?", "answer": "magikarp"},
#     {"q": "I sleep all day, blocking roads. Who am I?", "answer": "snorlax"},
#     {"q": "I’m a psychic cat, created in a lab. Who am I?", "answer": "mewtwo"},
#     {"q": "I evolve into Jolteon, Flareon, or Vaporeon. Who am I?", "answer": "eevee"},
#     {"q": "I’m shaped like a Poké Ball but I’m not one. Who am I?", "answer": "electrode"},
#     {"q": "I’m a ghost in Lavender Town’s tower. Who am I?", "answer": "gastly"},
#     {"q": "I’m always singing and putting others to sleep. Who am I?", "answer": "jigglypuff"},
#     {"q": "I have a skull on my head and cry for my mother. Who am I?", "answer": "cubone"},
#     {"q": "I’m the first Pokémon in the Pokédex. Who am I?", "answer": "bulbasaur"},
#     {"q": "I’m a fiery bird legendary from Kanto. Who am I?", "answer": "moltres"},
#     {"q": "I’m an ice bird legendary from Kanto. Who am I?", "answer": "articuno"},
#     {"q": "I’m an electric bird legendary from Kanto. Who am I?", "answer": "zapdos"},
#     {"q": "I’m known as the 'Dragon Pokémon' and fly high. Who am I?", "answer": "dragonite"},
#     {"q": "I’m a fossil that comes back to life as a spiral. Who am I?", "answer": "omanyte"},
#     {"q": "I’m a fossil that comes back to life as a dome. Who am I?", "answer": "kabuto"},
#     {"q": "I look like a pink balloon but I’m a fighter at heart. Who am I?", "answer": "clefairy"},
#     {"q": "I spit fire and have wings but I’m not a Dragon type. Who am I?", "answer": "charizard"},
#     {"q": "I’m a blue turtle starter. Who am I?", "answer": "squirtle"},
#     {"q": "I’m a grass dinosaur starter. Who am I?", "answer": "bulbasaur"},
#     {"q": "I’m known as the Mouse Pokémon. Who am I?", "answer": "pikachu"},
#     {"q": "I can copy anyone’s moves. Who am I?", "answer": "ditto"},
#     {"q": "I was once called MissingNo. Who am I?", "answer": "missingno"},
#     {"q": "I’m a fire dog Pokémon that evolves with a Fire Stone. Who am I?", "answer": "growlithe"},
#     {"q": "I’m a small seed Pokémon that evolves into a flower. Who am I?", "answer": "oddish"},
#     {"q": "I live under the sea and evolve into Cloyster. Who am I?", "answer": "shellder"},
#     {"q": "I’m round, pink, and evolve into Chansey. Who am I?", "answer": "happiny"},
#     {"q": "I look like a rock snake. Who am I?", "answer": "onix"},
#     {"q": "I’m the Legendary Pokémon of Time. Who am I?", "answer": "dialga"},
#     {"q": "I’m the Legendary Pokémon of Space. Who am I?", "answer": "palkia"},
#     {"q": "I’m the Legendary Pokémon of Antimatter. Who am I?", "answer": "giratina"},
#     {"q": "I’m an Eevee evolution with water powers. Who am I?", "answer": "vaporeon"},
#     {"q": "I’m an Eevee evolution with fire powers. Who am I?", "answer": "flareon"},
#     {"q": "I’m an Eevee evolution with psychic powers. Who am I?", "answer": "espeon"},
#     {"q": "I’m an Eevee evolution with dark powers. Who am I?", "answer": "umbreon"},
#     {"q": "I’m an Eevee evolution with ice powers. Who am I?", "answer": "glaceon"},
#     {"q": "I’m an Eevee evolution with grass powers. Who am I?", "answer": "leafeon"},
#     {"q": "I’m an Eevee evolution with fairy powers. Who am I?", "answer": "sylveon"},
#     {"q": "I’m a floating magnet Pokémon. Who am I?", "answer": "magnemite"},
#     {"q": "I’m a punching Pokémon with boxing gloves. Who am I?", "answer": "hitmonchan"},
#     {"q": "I’m a kicking Pokémon with strong legs. Who am I?", "answer": "hitmonlee"},
#     {"q": "I’m a dragon-like Legendary Pokémon from Hoenn. Who am I?", "answer": "rayquaza"},
#     {"q": "I guard the seas as a Legendary Pokémon. Who am I?", "answer": "kyogre"},
#     {"q": "I guard the land as a Legendary Pokémon. Who am I?", "answer": "groudon"},
#     {"q": "I’m the Legendary Pokémon that represents the Sun. Who am I?", "answer": "solgaleo"},
#     {"q": "I’m the Legendary Pokémon that represents the Moon. Who am I?", "answer": "lunala"},
#     {"q": "I’m a fossil Pokémon that evolves into Armaldo. Who am I?", "answer": "anorith"},
#     {"q": "I’m a fossil Pokémon that evolves into Cradily. Who am I?", "answer": "lileep"},
#     {"q": "I’m a bug that evolves into a butterfly. Who am I?", "answer": "caterpie"},
#     {"q": "I’m a bug that evolves into a bee. Who am I?", "answer": "weedle"},
#     {"q": "I’m a Legendary Pokémon created from DNA splicing. Who am I?", "answer": "mewtwo"},
#     {"q": "I’m the Pokémon who cries when its mother is gone, wearing her skull. Who am I?", "answer": "cubone"}
# ]

# STATS_PATH = "question_stats.json"

# def load_letter_stats():
#     if os.path.exists(STATS_PATH):
#         try:
#             with open(STATS_PATH, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#                 return Counter(data.get("letter_counts", {}))
#         except Exception:
#             return Counter()
#     return Counter()

# def save_letter_stats(counter):
#     try:
#         with open(STATS_PATH, "w", encoding="utf-8") as f:
#             json.dump({"letter_counts": dict(counter)}, f, indent=2)
#     except Exception:
#         pass

# def pick_question(index=None):
#     if index is None:
#         return random.choice(QUESTIONS)  # ✅ return single dict
#     return QUESTIONS[index % len(QUESTIONS)]

# def mask_answer(answer, revealed_letters=None):
#     revealed_letters = {ch.lower() for ch in (revealed_letters or set())}
#     return "".join(ch if (not ch.isalpha()) or (ch.lower() in revealed_letters) else "_" for ch in answer)

# def update_stats_with_answer(letter):
#     # Track frequency of correctly guessed letters in answers
#     c = load_letter_stats()
#     if letter.isalpha():
#         c[letter.lower()] += 1
#     save_letter_stats(c)
#     return c

# questions.py
import random
from question_banks import QUESTIONS

def pick_question(category, difficulty):
    """Picks a random question from the given category and difficulty."""
    try:
        # Attempt to get the list of questions for the specified category and difficulty
        questions_list = QUESTIONS.get(category, {}).get(difficulty, [])
        if questions_list:
            return random.choice(questions_list)
        
        # Fallback: If no questions for that difficulty, try any from the same category
        all_in_category = [q for diff_list in QUESTIONS.get(category, {}).values() for q in diff_list]
        if all_in_category:
            return random.choice(all_in_category)

    except (KeyError, IndexError):
        pass # Fallthrough to the general fallback

    # General Fallback: If category or difficulty fails, pick any question from General Knowledge
    all_questions = [q for diff_list in QUESTIONS["General Knowledge"].values() for q in diff_list]
    return random.choice(all_questions) if all_questions else {"q": "Default question?", "answer": "default"}