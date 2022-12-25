from abc import ABC, abstractmethod
from headers_enum import Headers
import regex

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
                    for word in regex.findall('\p{alpha}+', words):
                        for letter in word:
                            yield letter.upper()

    @abstractmethod
    def count(self):
        pass

class ExactCounter(Counter):
    def __init__(self, filename: str, stopwords: str):
        super().__init__(filename, stopwords)
    
    def count(self):
        letters = dict()

        for letter in self.read_letters():
            if letter not in letters.keys():
                letters[letter] = 1
            else:
                letters[letter] += 1 


        print("unique letters: ", len(letters))

        print("letters:", letters)
            
        return sum(letters.values())

def DecreasingProbabilityCounter(Counter):
    pass

def FrequentCounter(Counter):
    pass