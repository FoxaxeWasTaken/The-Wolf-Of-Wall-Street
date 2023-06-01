#!/usr/bin/env python3

import sys
import os
import tempfile

from tests_engine import get_algo_results, get_results, print_results


"""
Get the results of the current algorithm without having to wait for the end of the game
"""


def generate_empty_file_path():
    temp_dir = tempfile.gettempdir()
    while True:
        temp_filename = next(tempfile._get_candidate_names())
        temp_filepath = os.path.join(temp_dir, temp_filename)
        if not os.path.exists(temp_filepath):
            with open(temp_filepath, 'w'):
                pass
            return temp_filepath


def print_usage(prog_name: str):
    print("USAGE")
    print(f"\t{prog_name} [algo] [candles]")
    print("DESCRIPTION")
    print("\talgo\t\tThe algorithm to test")
    print("\tcandles\t\tThe path to the candles file")


def get_args(args: list):
    algo = "./trade" if len(args) == 0 else args[0]
    candles = "tests/candles/training-set_USDT_BTC-1.csv" if len(args) <= 1 else args[1]
    return algo, candles


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print_usage(sys.argv[0])
        sys.exit(84)
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print_usage(sys.argv[0])
        sys.exit(0)
    try:
        algo, candles = get_args(sys.argv[1:])
        result_file = generate_empty_file_path()
        get_algo_results(algo, candles, result_file)
        parsed_results = get_results(result_file)
        print_results(parsed_results)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(84)
