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


class AlgoStrategy():

    def __init__(self, strategy):
        self.cerebro = bt.Cerebro()
        strategy.init_broker(self.cerebro.broker)
        data = strategy.add_data(self.cerebro)
        strategy.data = data

        self.cerebro.addstrategy(strategy)

        self.portfolioStartValue = self.cerebro.broker.getvalue()
        self.cerebro.addanalyzer(btanalyzers.DrawDown, _name='dd')
        self.cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharpe')
        self.cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
        self.cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='ta')

    def performance(self):
        analyzer = self.thestrat.analyzers.ta.get_analysis()
        dd_analyzer = self.thestrat.analyzers.dd.get_analysis()

        # Get the results we are interested in
        total_open = analyzer.total.open
        total_closed = analyzer.total.closed
        total_won = analyzer.won.total
        total_lost = analyzer.lost.total
        win_streak = analyzer.streak.won.longest
        lose_streak = analyzer.streak.lost.longest
        pnl_net = round(analyzer.pnl.net.total, 2)
        strike_rate = 0
        if total_closed > 0:
            strike_rate = (total_won / total_closed) * 100
        # Designate the rows
        h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
        h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
        h3 = ['DrawDown Pct', 'MoneyDown', '', '']
        self.total_closed = total_closed
        self.strike_rate = strike_rate
        self.max_drawdown = dd_analyzer.max.drawdown
        r1 = [total_open, total_closed, total_won, total_lost]
        r2 = [('%.2f%%' % (strike_rate)), win_streak, lose_streak, pnl_net]
        r3 = [('%.2f%%' % (dd_analyzer.max.drawdown)), dd_analyzer.max.moneydown, '', '']
        # Check which set of headers is the longest.
        header_length = max(len(h1), len(h2), len(h3))
        # Print the rows
        print_list = [h1, r1, h2, r2, h3, r3]
        row_format = "{:<15}" * (header_length + 1)
        print("Trade Analysis Results:")
        for row in print_list:
            print(row_format.format('', *row))

        analyzer = self.thestrat.analyzers.sqn.get_analysis()
        sharpe_analyzer = self.thestrat.analyzers.sharpe.get_analysis()
        self.sqn = analyzer.sqn
        self.sharpe_ratio = sharpe_analyzer['sharperatio']
        if self.sharpe_ratio is None:
            self.sharpe_ratio = 0
        self.pnl = self.cerebro.broker.getvalue() - self.portfolioStartValue
        print('[SQN:%.2f, Sharpe Ratio:%.2f, Final Portfolio:%.2f, Total PnL:%.2f]' % (
        self.sqn, self.sharpe_ratio, self.cerebro.broker.getvalue(), self.pnl))

    def run(self):
        thestrats = self.cerebro.run()
        self.thestrat = thestrats[0]
        self.performance()
