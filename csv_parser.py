from pprint import pprint

import pandas as pd
import os
import glob
import csv


class CsvParser:

    def __init__(self, path: str):
        self._path = path
        self._csv_files = glob.glob(os.path.join(path, "*.csv"))
        self._train_data = self._setup_train_data(60)
        # pprint(self._extract_file(self._csv_files[1]))

    def get_all(self):
        result = []
        for f in self._csv_files:
            result.extend(self._extract_file(f))
        return result

    def get_one(self, ticker_name, timeframe):
        for f in self._csv_files:
            tn, tf = self._get_file_info(f)
            if tn == ticker_name and tf == timeframe:
                return self._extract_file(f)
        return []

    def get_for_train(self):
        import random
        ticker_name, data = random.choice(self._train_data)
        return ticker_name, data

    def _extract_file(self, filename):
        ticker_name, timeframe = self._get_file_info(filename)
        if timeframe == -1:
            return []
        result = []
        with open(filename, "r") as _file:
            reader = csv.reader(_file, delimiter=' ', quotechar='|')
            row: str
            _first_row = True
            for row in reader:
                if _first_row:
                    _first_row = False
                    continue
                _date, _time, _open, _high, _low, _close, _tick_vol, _vol, _spread = row[0].split("\t")
                _datetime = self._reformat_datetime(_date, _time)
                point = {
                    "table": "tickers",
                    "ticker_name": ticker_name,
                    "timeframe": timeframe,
                    "time": _datetime,
                    "fields": {
                        "high": _high,
                        "close": _close,
                        "low": _low,
                        "open": _open,
                        "volume": _vol
                    }
                }
                result.append(point)
        return result

    def _get_file_info(self, filename: str):
        ticker_name, _timeframe, _, _ = filename.split("\\")[-1].replace(".csv", "").split("_")
        timeframe = self._reformat_timeframe(_timeframe)
        return ticker_name, timeframe

    def _setup_train_data(self, timeframe: int) -> list:
        result = []
        for f in self._csv_files:
            tn, tf = self._get_file_info(f)
            if tf == timeframe:
                result.append((tn, self._extract_file(f)))
        return result

    @staticmethod
    def _reformat_timeframe(raw_timeframe: str):
        if raw_timeframe == 'M5':
            return 5
        elif raw_timeframe == 'M15':
            return 15
        elif raw_timeframe == 'M30':
            return 30
        elif raw_timeframe == 'H1':
            return 60
        elif raw_timeframe == 'H4':
            return 240
        else:
            return -1

    @staticmethod
    def _reformat_datetime(date: str, time: str):
        return f'{date.replace(".", "-")} {time}'
