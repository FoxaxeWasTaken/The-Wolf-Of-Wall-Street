import json
import sys


from chart import Chart


class Config:
    def __init__(self, path: str) -> None:
        self.__path = path
        self.__config = {}
        self.__load()
        if "pauseOnBoundsSell" not in self.__config:
            self.__config["pauseOnBoundsSell"] = 3
        if "signals" not in self.__config:
            self.__config["signals"] = []
        if "buyOn" not in self.__config:
            self.__config["buyOn"] = []
        self.__check_config()

    def __load(self) -> None:
        with open(self.__path) as f:
            self.__config = json.load(f)

    def __check_config(self) -> None:
        for signal in self.__config["signals"]:
            for values in self.__config["signals"][signal]:
                assert len(values) == 3
        for buyOnConfig in range(len(self.__config["buyOn"])):
            assert "conditions" in self.__config["buyOn"][buyOnConfig]
            assert "risk" in self.__config["buyOn"][buyOnConfig]
            if "stop_loss" not in self.__config["buyOn"][buyOnConfig]:
                self.__config["buyOn"][buyOnConfig]["stop_loss"] = 0
            if "take_profit" not in self.__config["buyOn"][buyOnConfig]:
                self.__config["buyOn"][buyOnConfig]["take_profit"] = 10000000
            if "trailing_stop_loss" not in self.__config["buyOn"][buyOnConfig]:
                self.__config["buyOn"][buyOnConfig]["trailing_stop_loss"] = None
            if "pause" not in self.__config["buyOn"][buyOnConfig]:
                self.__config["buyOn"][buyOnConfig]["pause"] = 0

    def check_on_chart(self, signal: str, chart: Chart) -> bool:
        for values in self.__config["signals"][signal]:
            right, cond, left = values
            if right in ["close", "high", "low", "volume"]:
                right = getattr(chart, right + "s")[-1]
            else:
                try:
                    right = chart.indicators[right][-1]
                except KeyError:
                    right = float(right)
            if left in ["close", "high", "low", "volume"]:
                left = getattr(chart, left + "s")[-1]
            else:
                try:
                    left = chart.indicators[left][-1]
                except KeyError:
                    left = float(left)

            if cond == ">":
                if right < left:
                    return False
            elif cond == "<":
                if right > left:
                    return False
        return True

    def get_buy_on(self) -> dict:
        return self.__config["buyOn"]

    def check_conditions(self, conditions: list, chart: Chart) -> bool:
        for condition in conditions:
            if not self.check_on_chart(condition, chart):
                return False
        return True
