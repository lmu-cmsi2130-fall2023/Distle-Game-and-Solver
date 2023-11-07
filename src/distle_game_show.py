'''
Empirical tester / basic interactive game running for having either a human
or AI play the game of Distle with a set of configurable parameters.

[!] Useful for debugging what's happening with particular words or to just
have fun playing the game! It is fun. You are required to agree for the
duration of this course.
'''

from distle_game import *

# Number of tries the player gets to guess the secret word
MAX_GUESSES: int = 10

# Number of games to be played, useful for testing any random
# elements of your player
N_GAMES: int = 1

# The secret word to be guessed, which can be either:
#    - A str that you hard-code for testing purposes
#    - Left as None to select a random word
WORD: Optional[str] = None

# Whether or not the game's individual steps / guesses / feedback are
# printed to the terminal
VERBOSE: bool = True

# Whether or not the game should be played by a human at the terminal (False)
# or your AI DistlePlayer (True)
AI_PLAYER: bool = False

# The path to the dictionary file that you wish to play from
DICTIONARY_PATH: str = "../dat/dictionary14.txt"

# Main game loop begun below!
game = DistleGame(DICTIONARY_PATH, VERBOSE, DistlePlayer() if AI_PLAYER else None)
victories = 0
for g in range(N_GAMES):
    if VERBOSE:
        print("[!] Game Starting: " + str(g+1) + " / " + str(N_GAMES))
    victories += 1 if game.new_game(MAX_GUESSES, WORD) else 0

print("=================================")
print("= Won: " + str(victories) + " / " + str(N_GAMES))
print("=================================")
