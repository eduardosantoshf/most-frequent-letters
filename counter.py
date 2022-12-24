from abc import ABC, abstractmethod
import re

class Counter(ABC):
    def __init__(self, filename: str, stopwords: str):
        self.filename = filename
        self.stopwords = set()

        with open(stopwords, 'r') as file:
            for word in file:
                self.stopwords.add(word.strip())

    def read_letters(self):
        with open(self.filename, 'r') as fp:
            for line in fp:
                for words in line.split():
                    # remove all stop-words and punctuation marks
                    for word in re.sub(r'[^a-zA-Z]', ' ', words).upper().split():
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