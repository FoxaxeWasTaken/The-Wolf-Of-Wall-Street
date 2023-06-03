import sys


def print_buy(pair: str, amount: float):
    print("COMMAND BUY", amount, pair, file=sys.stderr)
    print(f"buy {pair} {amount}", flush=True)


def print_sell(pair: str, amount: float):
    print("COMMAND SELL", amount, pair, file=sys.stderr)
    print(f"sell {pair} {amount}", flush=True)


class Stack:
    def __init__(
        self,
        amount: float,
        closing_price: float,
        stop_loss: float,
        take_profit: float,
        pair: str,
        transactionFee: float,
        trailing_stop_loss: float = None,
    ):
        self.amount = amount * (1 - (transactionFee / 100))
        self.closing_price = closing_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.pair = pair
        self.transactionFee = transactionFee
        self.trailing_stop_loss = trailing_stop_loss
        print("CREATED STACK", self, file=sys.stderr, flush=True)
        print_buy(pair, amount)

    def update(self, current_closing_price):
        if self.trailing_stop_loss is not None:
            if (
                current_closing_price == self.closing_price
                or current_closing_price < self.closing_price
            ):
                return
            delta = (current_closing_price - self.closing_price) / self.closing_price
            if delta >= self.trailing_stop_loss:
                self.stop_loss += self.stop_loss * self.trailing_stop_loss
                self.closing_price = current_closing_price
                print("UPDATED STACK STOP LOSS", self, file=sys.stderr, flush=True)
                return

    def is_out_of_bounds(self, closing_price):
        if closing_price <= self.stop_loss or closing_price >= self.take_profit:
            return True
        return False

    def __repr__(self):
        return f"Stack({self.amount} {self.stop_loss} {self.take_profit} {self.pair})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Stack):
            return (
                self.amount == __value.amount
                and self.stop_loss == __value.stop_loss
                and self.take_profit == __value.take_profit
                and self.pair == __value.pair
            )
        return False

    def __hash__(self) -> int:
        return hash((self.amount, self.stop_loss, self.take_profit, self.pair))


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
        self._update_emas()
        self._update_smas()
        self._update_stdevs()
        self._update_bollingers()
        self._update_rsis()

    def _update_emas(self):
        for window in [20, 50, 100, 200]:
            if f"ema{window}" not in self.indicators:
                self.indicators[f"ema{window}"] = []
            if len(self.closes) >= window:
                self.indicators[f"ema{window}"].append(self._ema(window))
            else:
                self.indicators[f"ema{window}"].append(None)

    def _update_smas(self):
        for window in [5, 8, 13, 21]:
            if f"sma{window}" not in self.indicators:
                self.indicators[f"sma{window}"] = []
            if len(self.closes) >= window:
                self.indicators[f"sma{window}"].append(self._sma(window))
            else:
                self.indicators[f"sma{window}"].append(None)

    def _update_stdevs(self):
        for window in [20]:
            if f"stdev{window}" not in self.indicators:
                self.indicators[f"stdev{window}"] = []
            if len(self.closes) >= window:
                self.indicators[f"stdev{window}"].append(self._stdev(window))
            else:
                self.indicators[f"stdev{window}"].append(None)

    def _update_bollingers(self):
        for sma_window in [20]:
            for stdevs_count in [1, 1.5, 2]:
                if f"bollinger{stdevs_count}_{sma_window}_upper" not in self.indicators:
                    self.indicators[f"bollinger{stdevs_count}_{sma_window}_upper"] = []
                    self.indicators[f"bollinger{stdevs_count}_{sma_window}_middle"] = []
                    self.indicators[f"bollinger{stdevs_count}_{sma_window}_lower"] = []
                if len(self.closes) >= sma_window:
                    upper, middle, lower = self._bollinger(sma_window, stdevs_count)
                    self.indicators[
                        f"bollinger{stdevs_count}_{sma_window}_upper"
                    ].append(upper)
                    self.indicators[
                        f"bollinger{stdevs_count}_{sma_window}_middle"
                    ].append(middle)
                    self.indicators[
                        f"bollinger{stdevs_count}_{sma_window}_lower"
                    ].append(lower)
                else:
                    self.indicators[
                        f"bollinger{stdevs_count}_{sma_window}_upper"
                    ].append(None)
                    self.indicators[
                        f"bollinger{stdevs_count}_{sma_window}_middle"
                    ].append(None)
                    self.indicators[
                        f"bollinger{stdevs_count}_{sma_window}_lower"
                    ].append(None)

    def _update_rsis(self):
        for window in [9, 14, 21]:
            if f"rsi{window}" not in self.indicators:
                self.indicators[f"rsi{window}"] = []
            if len(self.closes) >= window:
                self.indicators[f"rsi{window}"].append(self._rsi(window))
            else:
                self.indicators[f"rsi{window}"].append(None)

    def _ema(self, window):
        if len(self.closes) < window:
            return None
        if len(self.closes) == window:
            return self._sma(window)
        multiplier = 2 / (window + 1)
        previous_ema = self.indicators[f"ema{window}"][-1]
        return (self.closes[-1] - previous_ema) * multiplier + previous_ema

    def _sma(self, window):
        if len(self.closes) < window:
            return None
        return sum(self.closes[-window:]) / window

    def _stdev(self, window):
        if len(self.closes) < window:
            return None
        sma = self._sma(window)
        variance = sum([(close - sma) ** 2 for close in self.closes[-window:]]) / window
        return variance**0.5

    def _bollinger(self, sma_window, stdevs_count):
        if len(self.closes) < sma_window:
            return None
        sma = self._sma(sma_window)
        stdev = self._stdev(sma_window)
        return sma + stdevs_count * stdev, sma, sma - stdevs_count * stdev

    def _rsi(self, window):
        if len(self.closes) < window:
            return None

        gains = []
        losses = []

        for i in range(1, window):
            change = self.closes[-i] - self.closes[-i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        average_gain = sum(gains) / window
        average_loss = sum(losses) / window

        if average_loss == 0:
            return 100

        relative_strength = average_gain / average_loss
        rsi = 100 - (100 / (1 + relative_strength))

        return rsi
