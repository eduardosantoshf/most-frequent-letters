import time
import numpy as np

from counter import *

def decreasing_vs_exact():
    tests_number = 100
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

    # one line because if split onto multiple lines there is a bug when printing
    print(f"\n{'Letter':^5s} {'Value':^10s} {'Exact Value':<15s} {'Expected Value':<10s} {'MeanAE':>15s} {'MinAE':>15s} {'MaxAE':>15s} {'MeanRE':>16s} {'MinRE':>16s} {'MaxRE':>11s} {'StandDev':>15s} {'Variance':>15s}") 

    for letter in stats.keys():
        exact_value = exact_counter.letters[letter]

        l = np.array(expected_vals[letter])

        letter_val = np.mean(stats[letter])

        letter_expected_val = np.mean(expected_vals[letter])

        mean_absolute_error = np.mean(np.abs(exact_value - l))
        min_absolute_error = np.amin(np.abs(exact_value - l))
        max_absolute_error = np.amax(np.abs(exact_value - l))

        mean_relative_error = (mean_absolute_error / exact_value) * 100
        min_relative_error = (min_absolute_error / exact_value) * 100
        max_relative_error = (max_absolute_error / exact_value) * 100

        standard_deviation = np.std(expected_vals[letter])
        variance = np.var(expected_vals[letter])

        # one line because if split onto multiple lines there is a bug when printing
        print(f"{letter:^5s} {letter_val:^10.0f} {exact_value:^10.0f} {letter_expected_val:>15.0f} {mean_absolute_error:>20.1f} {min_absolute_error:>15.1f} {max_absolute_error:>15.1f} {mean_relative_error:>15.1f}% {min_relative_error:>15.1f}% {max_relative_error:>10.1f}% {standard_deviation:>15.3E} {variance:>15.3E}")
        
    final_time = time.time()

    print(final_time - initial_time)

def frequent_vs_exact():
    pass

if __name__ == "__main__":
    decreasing_vs_exact()