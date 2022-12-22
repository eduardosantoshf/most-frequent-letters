import argparse
from counter import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Most Frequent Letters')

    parser.add_argument(
        '-t',
        '--text',
        metavar = 'TEXT', 
        type = argparse.FileType('r'),
        help = 'Load literary work from text file'
    )

    parser.add_argument(
        '-s',
        '--stopwords',
        metavar = 'TEXT', 
        type = argparse.FileType('r'),
        help = 'Load stop-words from text file'
    )

    subparser = parser.add_subparsers(
        title='Counter type', 
        dest='counter-type',
        required = True, 
        help = 'Counter type/approach'
    )

    exact_parser = subparser.add_parser(
        'exact',
        help = 'Run with an exact counter'
    )

    decreasing_probability_parser = subparser.add_parser(
        'decreasing',
        help = 'Run with a counter based on a decreasing probability counter'
    )

    frequent_count_parser = subparser.add_parser(
        'frequent',
        help = 'Run with a counter based on frequent-count'
    )

args = vars(parser.parse_args())

if args['counter-type'] == 'exact':
        print(f"Running Exact Counter...")

        counter = ExactCounter(
            args['text'].name, 
            args['stopwords'].name
        )

        print(counter.count())