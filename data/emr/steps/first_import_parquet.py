import sys
from datetime import datetime

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

input_bucket='s3://firstratedata/'
input_path = '/us_stocks/1_minute_parquet/*.parquet'
df = spark.read.parquet(input_bucket + input_path)

df.show()

df = df.withColumn("datetime", df.datetime.cast(TimestampType()))

stonks = ["AAPL", "GOOG", "MSFT", "AMZN"]

df = df.where(df["sym"].isin(stonks))

df = df.withColumn("label", lit(0.0))

windowSpec = Window.orderBy("datetime").rowsBetween(-10,0)
df = df.withColumn('sma10', avg('close').over(windowSpec))

# More documentation about backtrader: https://www.backtrader.com/
dataLen=df.count()
dataLen

# Take 70% of data for training, use 30% of data for testing
trainLen=int(dataLen*0.7)
trainingData=spark.createDataFrame(df[:trainLen])
testData=spark.createDataFrame(df[trainLen:])
(trainingData.count(),testData.count())


from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.tuning import ParamGridBuilder
import numpy as np
from pyspark.ml.tuning import CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline
from time import *

feature_list = ["open", "high", "low", "close", "volume", "sma10"]
assembler = VectorAssembler(inputCols=feature_list, outputCol="features")
rf = RandomForestRegressor().setFeaturesCol("features").setLabelCol("label")
pipeline = Pipeline(stages=[assembler, rf])

#hyperparameters values: numTrees start, numTrees stop, numTrees num, maxDepth start, maxDepth stop, maxDepth num, numFolds
set1=[ 5, 25, 3, 5, 10, 3, 9]
set2=[ 10, 50, 3, 5, 10, 3, 9]
set3=[ 5, 25, 3, 5, 10, 3, 27]

params=[set1, set2, set3]
models=[]

for i in params:
    print("set" + str(i) )
    paramGrid = ParamGridBuilder() \
        .addGrid(rf.numTrees, [int(x) for x in np.linspace(start = i[0], stop = i[1], num = i[2])]) \
        .addGrid(rf.maxDepth, [int(x) for x in np.linspace(start = i[3], stop = i[4], num = i[5])]) \
        .build()

    crossval = CrossValidator(estimator=pipeline,
                              estimatorParamMaps=paramGrid,
                              evaluator=RegressionEvaluator(),
                              numFolds=i[6])

    starttime = time()
    m=crossval.fit(df)
    models.append(m)
    endtime = time()
    trainingtime = endtime - starttime
    print("Training time: %.3f seconds" % (trainingtime))

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


class MyFeed(DataBase):
    def __init__(self):
        super(MyFeed, self).__init__()
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

    class StrategyTemplate(bt.Strategy):

        def __init__(self):
            self.lastDay = -1
            self.lastMonth = -1
            self.dataclose = self.datas[0].close

        @staticmethod
        def init_broker(broker):
            pass

        @staticmethod
        def add_data(cerebro):
            pass

        def next(self):
            dt = self.datas[0].datetime.datetime(0)
            # print("[NEXT]:%s:close=%s" % (dt,self.dataclose[0]))

            # SOM
            if self.lastMonth != dt.month:
                if self.lastMonth != -1:
                    chg = self.broker.getvalue() - self.monthCash
                    # print("[%s] SOM:chg=%.2f,cash=%.2f" % (dt,chg,self.broker.getvalue()))
                self.lastMonth = dt.month
                self.monthCash = self.broker.getvalue()

                # SOD
            if self.lastDay != dt.day:
                self.lastDay = dt.day
                # print("[%s] SOD:cash=%.2f" % (dt,self.broker.getvalue()))

class MyStrategy(StrategyTemplate):

    def __init__(self):  # Initiation
        super(MyStrategy, self).__init__()

    def init_broker(broker):
        broker.setcash(1000000.0)
        broker.setcommission(commission=0.0)

    def add_data(cerebro):
        data = MyFeed()
        cerebro.adddata(data)
        return data

    def next(self):  # Processing
        super(MyStrategy, self).next()
        dt = self.datas[0].datetime.datetime(0)
        r = self.data.m[dt]
        # print(r)
        size = self.cerebro.strat_params['size']
        threshold_PctChg = self.cerebro.strat_params['pct_chg']

        model = self.cerebro.strat_params['model']
        df = spark.createDataFrame([r])
        sma = r['sma10']
        predictedSMA = model.transform(df).collect()[0]['prediction']
        expectedPctChg = (predictedSMA - SMA) / SMA * 100.0

        goLong = expectedPctChg > threshold_PctChg
        goShort = expectedPctChg < -threshold_PctChg
        # print("expectedPctChg=%s,goLong=%s,goShort=%s" % (expectedPctChg,goLong,goShort))

        if not self.position:
            if goLong:
                print("%s:%s x BUY @ %.2f" % (dt, size, r['close']))
                self.buy(size=size)  # Go long
            else:
                print("%s:%s x SELL @ %.2f" % (dt, size, r['close']))
                self.sell(size=size)  # Go short
        elif self.position.size > 0 and goShort:
            print("%s:%s x SELL @ %.2f" % (dt, size * 2, r['close']))
            self.sell(size=size * 2)
        elif self.position.size < 0 and goLong:
            print("%s:%s x BUY @ %.2f" % (dt, size * 2, r['close']))
            self.buy(size=size * 2)

scenarios = []
for p in range(0, len(models)):
    for s in range(0, 1):
        c = {'scenario': (p + 1), "size": 100, "pct_chg": 0.01, "model": models[p],
             'model_name': 'model.%s' % (p + 1)}
        print(c)
    scenarios.append(c)

# run scenarios
best_config = None
best_pnl = None
n = 0
for c in scenarios:
    print("*** [%s] RUN SCENARIO:%s" % ((n + 1), c))
    config = c
    algo = AlgoStrategy(MyStrategy)
    algo.cerebro.strat_params = config
    algo.run()
    if best_pnl is None or best_pnl < algo.pnl:
        best_config = c
        best_pnl = algo.pnl
    n += 1
# best scenario
print("*** BEST SCENARIO ***:%s" % best_config)
algo = AlgoStrategy(MyStrategy)
algo.cerebro.strat_params = best_config
algo.run()