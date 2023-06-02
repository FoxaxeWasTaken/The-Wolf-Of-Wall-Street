import sys


def print_buy(pair: str, amount: float):
    print("A stack is being bought", file=sys.stderr)
    print(f"buy {pair} {amount}", flush=True)


def print_sell(pair: str, amount: float):
    print("A stack is being sold", file=sys.stderr)
    print(f"sell {pair} {amount}", flush=True)


class Stack:
    def __init__(
        self,
        amount: float,
        stop_loss: float,
        take_profit: float,
        pair: str,
        transactionFee: float,
    ):
        self.amount = amount * (1 - transactionFee)
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.pair = pair
        self.transactionFee = transactionFee
        print_buy(pair, amount)

    def is_out_of_bounds(self, closing_price):
        if closing_price <= self.stop_loss or closing_price >= self.take_profit:
            return True
        return False


class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        for i, key in enumerate(format):
            value = tmp[i]
            if key == "pair":
                self.pair = value
            if key == "date":
                self.date = int(value)
            if key == "high":
                self.high = float(value)
            if key == "low":
                self.low = float(value)
            if key == "open":
                self.open = float(value)
            if key == "close":
                self.close = float(value)
            if key == "volume":
                self.volume = float(value)

    def __repr__(self):
        return str(self.pair) + str(self.date) + str(self.close) + str(self.volume)


class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)
