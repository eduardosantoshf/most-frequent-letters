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

        for letter in letters_val.keys():
            stats[letter].append(letters_val[letter])
            expected_vals[letter].append(letters_expected_val[letter])

    

    print(f"\n{'Letter':^5s} {'Value':^10s} {'Exact Value':^10s} {'Expected Value':^20s} {'MeanAbsError':^15s} {'MinAbsError':^15} {'MaxAbsError':^15}") 

    for letter in stats.keys():
        exact_value = exact_counter.letters[letter]

        l = np.array(expected_vals[letter])

        mean_absolute_error = np.mean(np.abs(exact_value - l))
        min_absolute_error = np.amin(np.abs(exact_value - l))
        max_absolute_error = np.amax(np.abs(exact_value - l))

        letter_val = np.mean(stats[letter])

        letter_expected_val = np.mean(expected_vals[letter])

        print(f"{letter:^5} {letter_val:^10.0f} {exact_value:^10.0f} {letter_expected_val:^20.0f} {mean_absolute_error:^15.1f} {min_absolute_error:^15.1f} {max_absolute_error:^15.1f}")

        #break
        #print("\n", l)
        
    final_time = time.time()

    print(final_time - initial_time)

def frequent_vs_exact():
    pass

if __name__ == "__main__":
    decreasing_vs_exact()