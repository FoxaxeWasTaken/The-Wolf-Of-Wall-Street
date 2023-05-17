#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import random
import csv
import datetime
import sys

def print_usage(prog_name: str):
    print("USAGE")
    print("\t" + prog_name + " <num_candles> (<frequency> <filename>)")
    print()
    print("DESCRIPTION")
    print("\tnum_candles\tnumber of candles to generate")
    print("\tfrequency\tfrequency of the candles (ex: 1y, 1m, 1d, 1h, 1min) | default: 1h")
    print("\tfilename\tfile in which the candles will be stored (without extension) | default: sample.csv")

def get_args(args: list):
    num_candles = int(args[0])
    if len(args) == 1:
        frequency = "1h"
        filename = "sample.csv"
    else:
        frequency = args[1]
        filename = args[2] + ".csv"
    return num_candles, frequency, filename

def get_random_candles(pair: str, num_candles: int, frequency: str):
    currency_pair = yf.Ticker(pair)
    history = currency_pair.history(period="max")
    resampled_data = history.resample(frequency).ffill()
    total_candles = len(resampled_data)
    start_index = random.randint(0, total_candles - num_candles)
    candles = resampled_data.iloc[start_index : start_index + num_candles]
    return candles

def export_to_csv(candles: pd.DataFrame, filename: str):
    headers = ["pair", "date", "high", "low", "open", "close", "volume"]
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for index, candle in candles.iterrows():
            date = int(datetime.datetime.timestamp(index))
            row = ["USDT_BTC", date, candle["High"], candle["Low"], candle["Open"], candle["Close"], candle["Volume"]]
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 2:
        print_usage(sys.argv[0])
        sys.exit(84)
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print_usage(sys.argv[0])
        sys.exit(0)
    try:
        num_candles, frequency, filename = get_args(sys.argv[1:])
        candles = get_random_candles("USDT-BTC", num_candles, frequency)
        export_to_csv(candles, filename)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(84)
