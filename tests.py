import time
import numpy as np

from counter import *

def decreasing_vs_exact():
    tests_number = 100
    initial_time = time.time()

    exact_counter = ExactCounter(
        "texts/CrimeAndPunishment/en.txt", 
        "stopwords/en.txt"
    )

    exact_counter.count()

    frequent_counter = DecreasingProbabilityCounter(
        "texts/CrimeAndPunishment/en.txt", 
        "stopwords/en.txt"
    )

    frequent_counter.count()

    stats = {letter: [] for letter in frequent_counter.letters.keys()}
    expected_vals = {letter: [] for letter in frequent_counter.letters.keys()}
    
    for _ in range(0, tests_number):
        frequent_counter.count()
        letters_val = frequent_counter.letters
        letters_expected_val = frequent_counter.letters_counter

        for letter in letters_val.keys():
            stats[letter].append(letters_val[letter])
            expected_vals[letter].append(letters_expected_val[letter])

    # one line because if split onto multiple lines there is a bug when printing
    print(f"\n{'Letter':^5s} {'Value':^10s} {'Exact Value':<15s} {'Expected Value':<10s} {'MeanAE':>15s} {'MinAE':>15s} {'MaxAE':>15s} {'MeanRE':>16s} {'MinRE':>16s} {'MaxRE':>11s} {'StandDev':>15s} {'Variance':>15s}") 

    # order letters by value
    exact_counter.letters = dict(sorted(exact_counter.letters.items(), key=lambda x: x[1], reverse=True))

    for letter in exact_counter.letters.keys():
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

    execution_time = final_time - initial_time

    print("\nExecution time (for " + str(tests_number) + " trials): " + str(round(execution_time, 2)) + "s")

def frequent_vs_exact(k: int):
    initial_time = time.time()

    exact_counter = ExactCounter(
        "texts/CrimeAndPunishment/en.txt", 
        "stopwords/en.txt"
    )

    exact_counter.count()
    exact_count = exact_counter.letters

    frequent_counter = FrequentCounter(
        "texts/CrimeAndPunishment/en.txt", 
        "stopwords/en.txt",
        k
    )

    frequent_counter.count()
    sorted_exact_count = sorted(exact_counter.letters.items(), key=lambda x: x[1], reverse=True)

    letters_count = dict(sorted(frequent_counter.letters.items(), key=lambda x: x[1], reverse=True))

    print(f"\n{'Letter':^5s} {'Value':^10s} {'Exact Value':<15s}") 

    for letter in letters_count.keys():
        print(f"{letter:^5s} {letters_count[letter]:^10.0f} {exact_count[letter]:^10.0f}")

    final_time = time.time()

    execution_time = final_time - initial_time

    print("\nExecution time: " + str(round(execution_time, 2)) + "s")

if __name__ == "__main__":
    decreasing_vs_exact()
    #frequent_vs_exact(20)