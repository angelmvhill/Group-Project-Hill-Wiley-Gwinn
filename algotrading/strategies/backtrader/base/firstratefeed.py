import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
from backtrader.feed import DataBase
from backtrader import date2num
from backtrader import TimeFrame
import os
import pytz
from pytz import timezone
import json
import time
import itertools
import datetime

import sys
import os
#import boto3
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.functions import *
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window


class FirstRateFeed(DataBase):
    def __init__(self, df):
        super(FirstRateFeed, self).__init__()
        self.list = df.select("datetime", "open", "high", "low", "close", "volume", "sma10"
                                    ).collect()
        self.n = 0

        self.fromdate = self.list[0]['datetime']
        self.todate = self.list[len(self.list) - 1]['datetime']
        self.timeframe = bt.TimeFrame.Minutes
        print("from=%s,to=%s" % (self.fromdate, self.todate))

        self.m = {}
        # print(self.list)

    def start(self):
        # Nothing to do for this data feed type
        pass

    def stop(self):
        # Nothing to do for this data feed type
        pass

    def _load(self):
        if self.n >= len(self.list):
            return False

        r = self.list[self.n]
        self.lines.datetime[0] = date2num(r['datetime'])

        self.lines.open[0] = r['open']
        self.lines.high[0] = r['high']
        self.lines.low[0] = r['low']
        self.lines.close[0] = r['close']
        self.lines.volume[0] = r['volume']
        self.m[r['datetime']] = r

        self.n = self.n + 1
        return True