import unittest
import pytest
import random
from distle_game import *
import multiprocessing
from joblib import Parallel, delayed # type: ignore

# The number of rounds each dictionary will be run on, choosing a random word each time
# Grading Default: 100
GAMESHOW_ROUNDS: int = 100

# The max number of guesses your agent will have to guess the secret word each game
# Grading Default: 10
MAX_GUESSES: int = 10

# The random number seed to ensure that the words selected by the DistleGame are
# consistent with each playthrough. Can be set to:
#    - int: literally any int for consistent runs, though runs will be different
#           for different choices of numbers
#    - None: no seed is set, so the words will be different each time
# Grading Default: ??? (will be chosen for everyone's tests at grading-time)
SEED: Optional[int] = None

# To speed up the tests, if your computer has multiple processing cores,
# we'll devote all but one to it -- this will slow down other processes,
# but make sure the tests finish as fast as possibles
# Grading Default: ??? (your code should finish in time if N_CORES = 1)
N_CORES: int = min(multiprocessing.cpu_count()-1, 8) if multiprocessing.cpu_count() > 1 else 1

# Number of seconds your agent has to run all GAMESHOW_ROUNDS
# Grading Default: 200 if N_CORES >= 4 else 200 * (4 - N_CORES)
DISTLE_GAME_TIMEOUT: int = 200 if N_CORES >= 4 else 200 * (4 - N_CORES)

# Standardized error message to explain why thresholds are or are not met
RATIO_MESSAGE: str = "[X] Your player is currently not winning a high enough proportion of games for full credit"

def run_game_show(dict_path: str) -> list[bool]:
    '''
    Runs the game show with the parameters specified in the global constants above,
    and using the provided dictionary.
    
    [!] Employs parallel processing to run as many games in parallel as there are
    cores on your computer. Set N_CORES to 1 for easier debugging.
    
    Parameters:
        dict_path (str):
            The path to the dictionary containing the possible words in this DistleGame
    
    Returns:
        list[bool]:
            The list of games won specified as booleans (True = won, False = lost)
    '''
    game = DistleGame(dict_path, False, DistlePlayer())
    word_count = game.get_dictionary_size()
    rng = random.Random(SEED)
    rand_inds = [rng.randint(0, word_count-1) for _ in range(GAMESHOW_ROUNDS)]
    sim_results: list[bool] = Parallel(n_jobs=N_CORES, verbose=1)(delayed(run_game_show_round)(game, rand_inds[i]) for i in range(GAMESHOW_ROUNDS))
    return sim_results

def run_game_show_round(game: "DistleGame", rand_ind: int) -> bool:
    '''
    Runs a single round of the DistleGame; simple but used for parallel processing.
    
    Parameters:
        game (DistleGame):
            The game being run
        rand_ind (int):
            The index of the random word to be chosen for this game
            
    Returns:
        bool:
            Whether or not the player won this game
    '''
    return game.new_game(MAX_GUESSES, rand_ind = rand_ind)

class DistleTests(unittest.TestCase):
    """
    Unit tests for validating the DistlePlayer functionality. Notes:
    - If this is the set of tests provided in the solution skeleton, it represents an
      incomplete set that you are expected to add to to adequately test your submission!
    - Your correctness score on the assignment will be assessed by a more complete,
      grading set of unit tests.
    - A portion of your style grade will also come from proper type hints; remember to
      validate your submission using `mypy .` and ensure that no issues are found.
    """
    
    def report_results(self, win_list: list[bool]) -> float:
        '''
        Reports the percentage of wins run by each unit test.
        
        Parameters:
            win_list (list[bool]):
                The list of booleans indicating whether or not the player won each game.
        
        Returns:
            float:
                The percentage of won games.
        '''
        wins = sum([1 for game in win_list if game])
        print("[!] " + self._testMethodName + " Tests: " + str(wins) + " / " + str(GAMESHOW_ROUNDS))
        return float(wins) / GAMESHOW_ROUNDS
    
    @pytest.mark.timeout(DISTLE_GAME_TIMEOUT)
    def test_distle_player_dict_6(self) -> None:
        sim_results = run_game_show("../dat/dictionary6.txt")
        self.assertLessEqual(0.80, self.report_results(sim_results), RATIO_MESSAGE)
        
    @pytest.mark.timeout(DISTLE_GAME_TIMEOUT)
    def test_distle_player_dict_10(self) -> None:
        sim_results = run_game_show("../dat/dictionary10.txt")
        self.assertLessEqual(0.90, self.report_results(sim_results), RATIO_MESSAGE)
         
    @pytest.mark.timeout(DISTLE_GAME_TIMEOUT)
    def test_distle_player_dict_14(self) -> None:
        sim_results = run_game_show("../dat/dictionary14.txt")
        self.assertLessEqual(0.95, self.report_results(sim_results), RATIO_MESSAGE)

if __name__ == '__main__':
    unittest.main()