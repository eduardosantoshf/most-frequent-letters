from abc import ABC, abstractmethod
from collections import defaultdict
import random as rand
import regex
import math

from headers_enum import Headers

class Counter(ABC):
    def __init__(self, filename: str, stopwords: str):
        self.filename = filename
        self.stopwords = set()
        self._letter_counter = 0
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
        self.letter_counter = 0
        self.k = 0

    @property # getter
    def letters(self):
        return self._letters

    def add_letter(self, letter):
        self.letters[letter] += 1
    
    @property # getter
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = value

    @property # getter
    def letter_counter(self):
        return self._letter_counter

    @letter_counter.setter
    def letter_counter(self, value):
        self._letter_counter = value

    @abstractmethod
    def compute(self):
        pass

class ExactCounter(Counter):
    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def compute(self):
        for letter in self.read_letters(): self.add_letter(letter)

        print("unique letters: ", len(self.letters))

        print("total of letters: ", sum(self.letters.values()))

class DecreasingProbabilityCounter(Counter):
    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def compute(self):        
        base = math.sqrt(2)

        for letter in self.read_letters():
            probability = 1 / (base**self.k)

            if rand.random() < probability:
                self.k += 1

                self.add_letter(letter)

        self.letter_counter = int((base**self.k - base + 1) / (base - 1))

class FrequentCounter(Counter):
    pass