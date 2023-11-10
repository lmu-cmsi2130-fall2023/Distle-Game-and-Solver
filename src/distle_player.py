from edit_dist_utils import *
import random

class DistlePlayer:
    '''
    AI Distle Player! Contains all of the logic to automagically play
    the game of Distle with frightening accuracy (hopefully)
    '''
    
    def start_new_game(self, dictionary: set[str], max_guesses: int) -> None:
        '''
        Called at the start of every new game of Distle, and parameterized by
        the dictionary composing all possible words that can be used as guesses,
        only ONE of which is the correct Secret word that your agent must
        deduce through repeated guesses and feedback.
        
        [!] Should initialize any attributes that are needed to play the
        game, e.g., by saving a copy of the dictionary, etc.
        
        Parameters:
            dictionary (set[str]):
                The dictionary of words from which the correct answer AND any
                possible guesses must be drawn
            max_guesses (int):
                The maximum number of guesses that are available to the agent
                in this game of Distle
        '''
        # [!] TODO
        self.dictionary: set[str] = dictionary
        self.max_guesses: int = max_guesses
        self.guesses_made: int = 0
        self.possible_words: set[str] = dictionary
        return
    
    def make_guess(self) -> str:
        '''
        Requests a new guess to be made by the agent in the current game of Distle.
        Uses only the DistlePlayer's attributes that had been originally initialized
        in the start_new_game method.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Returns:
            str:
                The next guessed word from this DistlePlayer
        '''
        # [!] TODO
        
        if self.guesses_made == 0:
            return random.choice(list(self.dictionary))
        else:
            return random.choice(list(self.possible_words))
    
    def get_feedback(self, guess: str, edit_dist: int, transforms: list[str]) -> None:
        '''
        Called by the DistleGame after the DistlePlayer has made an incorrect guess.
        The feedback furnished is described in the parameters below. Your agent will
        use this feedback in an attempt to rule out as many remaining possible guess
        words as it can, through which it can then make better guesses in make_guess.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Parameters:
            guess (str):
                The last, incorrect guess made by this DistlePlayer
            edit_distance (int):
                The numerical edit distance between the guess your agent made and the
                secret word
            transforms (list[str]):
                The list of top-down transforms needed to turn the guess word into the
                secret word, i.e., the transforms that would be returned by your
                get_transformation_list(guess, secret_word)
        '''
        # [!] TODO

        words_to_remove: set[str] = set()
        word_ed: int
        word_trans: list[str]
        d: int = 0
        i: int = 0
        matches: bool = False
        
        for t in transforms:
            if t == 'D':
                d += 1
            if t == 'I':
                i += 1
            if d == i:
                matches = True
        if 'D' in transforms and 'I' not in transforms or 'I' in transforms and 'D' not in transforms:
            for word in self.possible_words:
                if 'D' in transforms and len(word) >= len(guess):
                    words_to_remove.add(word)
                elif 'I' in transforms and len(word) <= len(guess):
                    words_to_remove.add(word)
            self.possible_words -= words_to_remove
        elif 'D' not in transforms and 'I' not in transforms and not matches:
            for word in self.possible_words:
                if len(word) != len(guess):
                    words_to_remove.add(word)
            self.possible_words -= words_to_remove


        for word in self.possible_words:
            word_ed = edit_distance(guess, word)
            
            if edit_dist == word_ed:
                word_trans = get_transformation_list(guess, word)
                if transforms != word_trans:
                    words_to_remove.add(word)
            else:
                words_to_remove.add(word)
        self.possible_words -= words_to_remove

        return
