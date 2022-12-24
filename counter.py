from abc import ABC, abstractmethod
from headers_enum import Headers
import re

class Counter(ABC):
    def __init__(self, filename: str, stopwords: str):
        self.filename = filename
        self.stopwords = set()

        with open(stopwords, 'r') as file:
            for word in file:
                self.stopwords.add(word.strip())

    def read_letters(self):
        with open(self.filename, 'r') as file:
            while True:
                line = file.readline()

                # ignore the Project Gutenberg file headers
                if line.strip() in [header.value for header in Headers]: break
                
            while line:
                line = file.readline()

                for words in line.split():
                    # remove all stop-words and punctuation marks
                    for word in re.sub(r'[^0-9a-zA-Z]', ' ', words).upper().split():
                        for letter in word:
                            yield letter

    @abstractmethod
    def count(self):
        pass

class ExactCounter(Counter):
    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def count(self):
        letters = list()

        for letter in self.read_letters(): letters.append(letter)
            
        return len(letters)

def DecreasingProbabilityCounter(Counter):
    pass

def FrequentCounter(Counter):
    pass