import time
import numpy as np

from counter import *

def decreasing_vs_exact():
    tests_number = 5
    initial_time = time.time()

    exact_counter = ExactCounter(
        "texts/TheMetamorphosis/en.txt", 
        "stopwords/en.txt"
    )

    exact_counter.count()

    decreasing_counter = DecreasingProbabilityCounter(
        "texts/TheMetamorphosis/en.txt", 
        "stopwords/en.txt"
    )

    decreasing_counter.count()

    stats = {letter: [] for letter in decreasing_counter.letters.keys()}
    expected_vals = {letter: [] for letter in decreasing_counter.letters.keys()}
    
    for _ in range(0, tests_number):
        decreasing_counter.count()
        letters_val = decreasing_counter.letters
        letters_expected_val = decreasing_counter.letters_counter

        #print("\nTotal letters: ", letters_val)

        for letter in letters_val.keys():
            stats[letter].append(letters_val[letter])
            expected_vals[letter].append(letters_expected_val[letter])
        
    
    print("\nstats: ", stats)
    print("\nexpected_vals: ", expected_vals)

    final_time = time.time()

    for letter in stats.keys():
        exact_value = exact_counter.letters[letter]

        l = np.array(expected_vals[letter])

        mean_absolute_error = np.mean(np.abs(exact_value - l))
        min_absolute_error = np.amin(np.abs(exact_value - l))
        max_absolute_error = np.amax(np.abs(exact_value - l))

        print(mean_absolute_error)
        print(min_absolute_error)
        print(max_absolute_error)


        #print("\n", l)
        

    print(final_time - initial_time)

def frequent_vs_exact():
    pass

if __name__ == "__main__":
    decreasing_vs_exact()