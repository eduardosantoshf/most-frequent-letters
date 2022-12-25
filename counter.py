from abc import ABC, abstractmethod
from collections import defaultdict
import regex

from headers_enum import Headers

class Counter(ABC):
    def __init__(self, filename: str, stopwords: str):
        self.filename = filename
        self.stopwords = set()
        self.letters = defaultdict(lambda: 0)

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

    def add_letter(self, letter):
        self.letters[letter] += 1 

    @abstractmethod
    def count(self):
        pass

class ExactCounter(Counter):
    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def count(self):

        for letter in self.read_letters(): self.add_letter(letter)

        print("unique letters: ", len(self.letters))
        print("letters:", self.letters)
            
        return sum(self.letters.values())

def DecreasingProbabilityCounter(Counter):
    pass

def FrequentCounter(Counter):
    pass