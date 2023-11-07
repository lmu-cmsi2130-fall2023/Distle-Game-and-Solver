from edit_dist_utils import *
from distle_player import *
from typing import *
import random
import os
import copy

class DistleGame:
    '''
    Class responsible for managing the mechanics of a game of Distle, plus
    for managing the input sources, either a human or AI player
    '''

    def __init__(self, dictionary_path: str, verbose: bool, ai: Optional["DistlePlayer"]) -> None:
        '''
        Constructs a new DistleGame to play from the given dictionary.
        
        Parameters:
            dictionary_path (str):
                Path to a dictionary file with new-line separated words composing all possible
                words that may be selected as the secret answers.
            verbose (bool):
                Boolean flag that can be set to True to see all of the game's mechanics printed
                out, False otherwise
            ai (Optional[DistlePlayer]):
                Pass in a new DistlePlayer object to have it play the game; otherwise, leave as
                None to play as a human.
        '''
        self._ai: Optional["DistlePlayer"] = ai
        self._verbose: bool = verbose
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, dictionary_path)
        self.dictionary: set[str] = set()
        with open(file_path, "r") as file:
            for line in file:
                self.dictionary.add(line.rstrip())
        self.rand_word_list: list[str] = list(self.dictionary)
        self.rand_word_list.sort()
    
    def new_game(self, max_guesses: int, word: Optional[str] = None, rand_ind: Optional[int] = None) -> bool:
        '''
        Begins a new game of Distle with the specified word as the secret. The player must
        guess this word in at most max_guesses to win.
        
        Parameters:
            max_guesses (int):
                The maximum number of guesses that the player can make in this game.
            word (Optional[str]):
                The secret word to use for this game of Distle. Must be a word that
                exists in the dictionary, and if left as None, one will be chosen at random.
            rand_ind (Optional[int]):
                The index from the list of words to choose from, presumably generated
                randomly outside of this method
        
        Returns:
            bool:
                Whether or not the player won this game of Distle.
        '''
        if rand_ind is None:
            rand_ind = random.randint(0, self.get_dictionary_size()-1)
        if word is None:
            word = self.rand_word_list[rand_ind]
        if not word in self.dictionary: raise ValueError("[X] Word must be in the given dictionary, but was " + str(word))
        
        return self.initialize_game(max_guesses, word)
        
    def get_guess(self) -> str:
        '''
        Requests a guess for the secret word from the current game's DistlePlayer. If the player
        is human, accepts their answer via the terminal. If an AI, calls its make_guess method.
        
        Returns:
            str:
                The guess returned by the DistlePlayer.
        '''
        if self._ai is None:
            if self._verbose: print("  > Enter Guess Below > ")
            guess = input()
            return guess
        else:
            return self._ai.make_guess()
    
    def get_dictionary_size(self) -> int:
        '''
        Getter for the number of words contained in this game's dictionary.
        
        Returns:
            int:
                The number of words in this game's dictionary.
        '''
        return len(self.dictionary)
    
    def _end_game(self, won: bool, guess: str) -> bool:
        '''
        Reporting method largely for just keeping code DRY: reports on whether or not
        the player won the game and returns the resulting bool.
        
        Parameters:
            won (bool):
                Whether or not the player won the game.
            guess (str):
                The last guess the player made at the game's terminus.
        
        Returns:
            bool:
                Whether or not the player won.
        '''
        if won:
            self._won_game = True
            if self._verbose:
                if not self._ai is None: print("  > Enter Guess Below > \n" + guess)
                print("[W] You guessed correctly, congratulations!")
        else:
            if self._verbose: print("[L] Your word game is weak, too bad. The correct answer:\n" + self._word)
        return won
            
    def won_game(self) -> bool:
        '''
        Getter for whether or not the player won the game.
        
        Returns:
            bool:
                Whether or not the player has won the game.
        '''
        return self._won_game
            
    def initialize_game(self, max_guesses: int, word: str) -> bool:
        '''
        The main workhorse method of a newly started DistleGame that sequentially selects / sets
        a secret word, resets any game-tracking attributes, and then repeatedly asks the player
        for guesses until either the max have been expended or the player has won.
        
        Parameters:
            max_guesses (int):
                The maximum number of guesses the player has to make.
            word (str):
                The secret word that the player must guess to win.
        
        Returns:
            bool:
                Whether or not the player won the game.
        '''
        self._word: str = word
        self._max_guesses: int = max_guesses
        self._guesses: int = 0
        self._won_game = False
        guess = ""
        
        if not self._ai is None:
            self._ai.start_new_game(copy.deepcopy(self.dictionary), max_guesses)
        
        if self._verbose:
            print("=================================")
            print("=       Welcome to Distle       =")
            print("=================================")
        
        while self._guesses < self._max_guesses:
            if self._verbose: print("[G] Guess " + str(self._guesses+1) + " / " + str(self._max_guesses))
            
            guess = self.get_guess()
            self._guesses += 1
            
            if not guess in self.dictionary:
                if self._verbose: print("  [X] Word not in dictionary, try again (lost your turn lul)")
                continue
            
            table = get_edit_dist_table(guess, self._word)
            distance = table[len(guess)][len(self._word)]
            if distance == 0:
                return self._end_game(True, guess)
            
            transforms = get_transformation_list_with_table(guess, self._word, table)
            if not self._ai is None:
                if self._verbose: print("  > Enter Guess Below > \n" + guess)
                self._ai.get_feedback(guess, distance, transforms)
            
            if self._verbose and not self._guesses == self._max_guesses:
                print("  [~] Not quite, here are some hints:")
                print("    [!] Edit Distance: " + str(distance))
                print("    [!] Transforms (top-down): " + str(transforms))
                
        return self._end_game(False, guess)