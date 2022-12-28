from abc import ABC, abstractmethod
from collections import defaultdict
import random as rand
import regex
import math

from headers_enum import Headers
from footers_enum import Footers

class Counter(ABC):
    """Superclass representing Counter"""

    def __init__(self, filename: str, stopwords: str):
        self.filename = filename
        self.stopwords = set()
        self._letters_counter = dict()
        self._k = 0 # counter value
        self._letters = defaultdict(lambda: 0)

        with open(stopwords, 'r') as file:
            for word in file:
                self.stopwords.add(word.strip())

    def read_letters(self):
        with open(self.filename, 'r') as file:
            while True:
                line = file.readline()

                # ignore the Project Gutenberg's file headers
                if line.strip() in [header.value for header in Headers]: break
                
            while line:
                line = file.readline()

                # ignore the Project Gutenberg's file footers
                if line.strip() in [footer.value for footer in Footers]: break

                for words in line.split():
                    # remove all stop-words and punctuation marks
                    for word in regex.findall('\p{alpha}+', words):
                        for letter in word:
                            yield letter.upper()
    
    def count(self):
        self.reset()
        self.compute()

    def reset(self):
        # reset variables for each run of a test
        self.letters_counter.clear()
        self.k = 0

    @property # getter
    def letters(self):
        return self._letters

    def add_letter(self, letter):
        self.letters[letter] += 1

    @letters.setter
    def letters(self, letters):
        self._letters = letters
    
    @property # getter
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = value

    @property # getter
    def letters_counter(self):
        return self._letters_counter

    @abstractmethod
    def compute(self):
        pass

class ExactCounter(Counter):
    """Class representing Exact Counter"""

    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def compute(self):
        for letter in self.read_letters(): self.add_letter(letter)

        print("\nTotal letters: ", sum(self.letters.values()))

class DecreasingProbabilityCounter(Counter):
    """Class representing Decreasing Probability Counter"""
    
    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def compute(self):        
        base = math.sqrt(2)

        probabilities = dict()
        for letter in self.read_letters():
            self.k = self.letters[letter] # k = # of occurences of each letter 

            probabilities[letter] = 1 / (base**self.k)

            # if counter (letters[letter]) has value k, 
            # increment with probability 1 / (base**k)
            if rand.random() < probabilities[letter]: 
                self.add_letter(letter)

            # estimate the number of events (letters) from the counter value, k?
            # compute (base**k – base + 1) / (base – 1) (slides)
            self.letters_counter[letter] = int((base**self.k - base + 1) / (base - 1))

class FrequentCounter(Counter):
    """Class representing Frequent Counter"""

    def __init__(self, filename: str, stopwords: str, k: int):
        super().__init__(filename, stopwords)
        self.counters = defaultdict(lambda: 0)
        self.k_parameter = k
    
    def compute(self): 
        k = self.k_parameter

        letters = list()

        # Misra & Gries algorithm
        for letter in self.read_letters():
            if letter not in letters: letters.append(letter)

            # case 1: item already has counter or there are empty counters
            # keeps, at most, (k – 1) candidates at the same time
            # candidate: item that occurs more than a 1/k fraction of 
            # the time in the input
            if letter in self.counters.keys() or (len(self.counters.keys()) < (k - 1)): 
                self.counters[letter] += 1
            
            ## case 2: item doesn't have counter and there are no empty counters
            else:
                for letter, count in list(self.counters.items()):
                    self.counters[letter] -= 1
                    
                    if count == 0: del self.counters[letter]

        # if letter in counters[letter] then 
        # frequency_estimate[letter] = counters[letter]
        # else frequency_estimate[letter] = 0
        counts = [self.counters[letter] if self.counters[letter] else 0 for letter in letters]

        self.letters = {letter: count for letter, count in zip(letters, counts)}