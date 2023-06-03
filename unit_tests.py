import unittest
import sys

from io import StringIO

from chart import Chart, Candle, Stack, print_buy, print_sell


class TestCaptureStdout(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCaptureStdout, self).__init__(*args, **kwargs)
        self.captured_output = StringIO()

    def capture_stdout(self):
        sys.stdout = self.captured_output

    def get_captured_output(self):
        return self.captured_output.getvalue()

    def check_stdout(self, expected_output):
        self.assertEqual(self.get_captured_output(), expected_output)

    def check_in_stdout(self, expected_output):
        self.assertIn(expected_output, self.get_captured_output())

    def release_stdout(self):
        sys.stdout = sys.__stdout__


class TestStack(TestCaptureStdout):
    def tests_stack_creation(self):
        self.capture_stdout()
        stack = Stack(100, 667, 1, 2, "BTCUSDT", 0.001)
        self.release_stdout()
        self.check_stdout("buy BTCUSDT 100\n")
        self.assertAlmostEqual(stack.amount, 99.999)
        self.assertAlmostEqual(stack.stop_loss, 1)
        self.assertAlmostEqual(stack.take_profit, 2)
        self.assertEqual(stack.pair, "BTCUSDT")
        self.assertAlmostEqual(stack.transactionFee, 0.001)

    def tests_stack_is_out_of_bounds(self):
        self.capture_stdout()
        stack = Stack(100, 667, 1, 2, "BTCUSDT", 0.001)
        self.release_stdout()
        self.check_stdout("buy BTCUSDT 100\n")
        self.assertEqual(stack.is_out_of_bounds(0.5), True)
        self.assertEqual(stack.is_out_of_bounds(2.5), True)
        self.assertEqual(stack.is_out_of_bounds(1.1), False)
        self.assertEqual(stack.is_out_of_bounds(1.9), False)


class TestCandle(TestCaptureStdout):
    def test_candle_initialization(self):
        data = "BTC/USD,12345,38500.0,37000.0,37500.0,38000.0,1000.0"
        format = ["pair", "date", "high", "low", "open", "close", "volume"]
        candle = Candle(format, data)
        
        self.assertEqual(candle.pair, "BTC/USD")
        self.assertEqual(candle.date, 12345)
        self.assertAlmostEqual(candle.high, 38500.0)
        self.assertAlmostEqual(candle.low, 37000.0)
        self.assertAlmostEqual(candle.open, 37500.0)
        self.assertAlmostEqual(candle.close, 38000.0)
        self.assertAlmostEqual(candle.volume, 1000.0)
    
    def test_candle_representation(self):
        data = "ETH/BTC,12345,0.04,0.03,0.035,0.036,500.0"
        format = ["pair", "date", "high", "low", "open", "close", "volume"]
        candle = Candle(format, data)
        
        expected_repr = "ETH/BTC123450.036500.0"
        self.assertEqual(repr(candle), expected_repr)


class TestPrintBuy(TestCaptureStdout):
    def test_print_buy(self):
        self.capture_stdout()
        print_buy("BTC/USD", 100)
        self.release_stdout()
        self.check_stdout("buy BTC/USD 100\n")

    def test_print_buy_2(self):
        self.capture_stdout()
        print_buy("ETH/BTC", 0.5)
        self.release_stdout()
        self.check_stdout("buy ETH/BTC 0.5\n")


class TestPrintSell(TestCaptureStdout):
    def test_print_sell(self):
        self.capture_stdout()
        print_sell("BTC/USD", 100)
        self.release_stdout()
        self.check_stdout("sell BTC/USD 100\n")

    def test_print_sell_2(self):
        self.capture_stdout()
        print_sell("ETH/BTC", 0.5)
        self.release_stdout()
        self.check_stdout("sell ETH/BTC 0.5\n")

class TestChart(TestCaptureStdout):
    def test_chart_creation(self):
        chart = Chart()
        
        self.assertEqual(chart.dates, [])
        self.assertEqual(chart.opens, [])
        self.assertEqual(chart.highs, [])
        self.assertEqual(chart.lows, [])
        self.assertEqual(chart.closes, [])
        self.assertEqual(chart.volumes, [])
        self.assertEqual(chart.indicators, {})

    def test_add_candle(self):
        chart = Chart()
        candle = Candle(["pair", "date", "high", "low", "open", "close", "volume"], "BTC/USD,1234876278,40000.0,39000.0,39500.0,39800.0,2000.0")
        chart.add_candle(candle)

        self.assertEqual(chart.dates, [1234876278])
        self.assertEqual(chart.opens, [39500.0])
        self.assertEqual(chart.highs, [40000.0])
        self.assertEqual(chart.lows, [39000.0])
        self.assertEqual(chart.closes, [39800.0])
        self.assertEqual(chart.volumes, [2000.0])
        self.assertEqual(len(chart.indicators["ema20"]), 1)
        self.assertEqual(chart.indicators["ema20"][0], None)
        self.assertEqual(len(chart.indicators["sma5"]), 1)
        self.assertEqual(chart.indicators["sma5"][0], None)
        self.assertEqual(len(chart.indicators["stdev20"]), 1)
        self.assertEqual(chart.indicators["stdev20"][0], None)
        self.assertEqual(len(chart.indicators["bollinger1_20_upper"]), 1)
        self.assertEqual(chart.indicators["bollinger1_20_upper"][0], None)
        self.assertEqual(len(chart.indicators["rsi9"]), 1)
        self.assertEqual(chart.indicators["rsi9"][0], None)
    
    def test_ema(self):
        chart = Chart()
        
        for i in range(50):
            close = 1000 + i
            candle = Candle(["pair", "date", "high", "low", "open", "close", "volume"], f"BTC/USD,{1234876278 + i},40000.0,39000.0,39500.0,{close},2000.0")
            chart.add_candle(candle)

        expected_ema50 = [None] * 49 + [1024.5]
        self.assertEqual(chart.indicators["ema50"], expected_ema50)
    
    def test_sma(self):
        chart = Chart()
        
        for i in range(5):
            close = 1000 + i
            candle = Candle(["pair", "date", "high", "low", "open", "close", "volume"], f"BTC/USD,{1234876278 + i},40000.0,39000.0,39500.0,{close},2000.0")
            chart.add_candle(candle)

        expected_sma5 = [None] * 4 + [1002.0]
        self.assertEqual(chart.indicators["sma5"], expected_sma5)
    
    def test_stdev(self):
        chart = Chart()
        
        for i in range(22):
            close = 1000 + i
            candle = Candle(["pair", "date", "high", "low", "open", "close", "volume"], f"BTC/USD,{1234876278 + i},40000.0,39000.0,39500.0,{close},2000.0")
            chart.add_candle(candle)

        expected_stdev20 = [None] * 19 + [5.766281297335398, 5.766281297335398, 5.766281297335398]
        self.assertEqual(chart.indicators["stdev20"], expected_stdev20)
    
    def test_bollinger(self):
        chart = Chart()
        
        for i in range(20):
            close = 1000 + i
            candle = Candle(["pair", "date", "high", "low", "open", "close", "volume"], f"BTC/USD,{1234876278 + i},40000.0,39000.0,39500.0,{close},2000.0")
            chart.add_candle(candle)

        expected_upper = [None] * 19 + [1015.2662812973354]
        expected_middle = [None] * 19 + [1009.5]
        expected_lower = [None] * 19 + [1003.7337187026646]
        self.assertEqual(chart.indicators["bollinger1_20_upper"], expected_upper)
        self.assertEqual(chart.indicators["bollinger1_20_middle"], expected_middle)
        self.assertEqual(chart.indicators["bollinger1_20_lower"], expected_lower)
        self.assertAlmostEqual(chart.indicators["bollinger2_20_upper"][-1], 1021.0325625946708)
        self.assertAlmostEqual(chart.indicators["bollinger2_20_middle"][-1], 1009.5)
        self.assertAlmostEqual(chart.indicators["bollinger2_20_lower"][-1], 997.9674374053292)
    
    def test_rsi(self):
        chart = Chart()
        
        for i in range(22):
            close = 1000 - i
            candle = Candle(["pair", "date", "high", "low", "open", "close", "volume"], f"BTC/USD,{1234876278 + i},40000.0,39000.0,39500.0,{close},2000.0")
            chart.add_candle(candle)

        expected_rsis = [None] * 20 + [0.0, 0.0]
        self.assertEqual(chart.indicators["rsi21"], expected_rsis)

if __name__ == "__main__":
    unittest.main()
