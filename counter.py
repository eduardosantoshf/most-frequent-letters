from abc import ABC, abstractmethod
import re

class Counter(ABC):
    def __init__(self, filename: str, stopwords: str):
        self.filename = filename
        self.stopwords = set()

        with open(stopwords, 'r') as file:
            for word in file:
                self.stopwords.add(word.strip())

    def read_words(self):
        with open(self.filename, 'r') as fp:
            for line in fp:
                for word in line.split():
                    # remove all stop-words and punctuation marks
                    for w in re.sub(r'[^a-zA-Z]', ' ', word).split():
                        yield w.upper()

    @abstractmethod
    def count(self):
        pass

class ExactCounter(Counter):
    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def count(self):
        words = set()

        for word in self.read_words(): words.add(word)
            
        return len(words)

def DecreasingProbabilityCounter(Counter):
    pass

def FrequentCounter(Counter):
    pass