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
        stack = Stack(100, 1, 2, "BTCUSDT", 0.001)
        self.release_stdout()
        self.check_stdout("buy BTCUSDT 100\n")
        self.assertEqual(stack.amount, 99.9)
        self.assertEqual(stack.stop_loss, 1)
        self.assertEqual(stack.take_profit, 2)
        self.assertEqual(stack.pair, "BTCUSDT")
        self.assertEqual(stack.transactionFee, 0.001)

    def tests_stack_is_out_of_bounds(self):
        self.capture_stdout()
        stack = Stack(100, 1, 2, "BTCUSDT", 0.001)
        self.release_stdout()
        self.check_stdout("buy BTCUSDT 100\n")
        self.assertEqual(stack.is_out_of_bounds(0.5), True)
        self.assertEqual(stack.is_out_of_bounds(2.5), True)
        self.assertEqual(stack.is_out_of_bounds(1.1), False)
        self.assertEqual(stack.is_out_of_bounds(1.9), False)


if __name__ == "__main__":
    unittest.main()
