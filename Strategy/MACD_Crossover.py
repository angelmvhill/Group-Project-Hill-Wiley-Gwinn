import backtrader.indicators as btind
import backtrader as bt
import datetime
import os

class MACD_Crossover(bt.Strategy):
    """
    This class serves as template for developing trading strategies using the MACD
    technical indicator. The buy logic is dependant on a crossover that occurs with
    the MACD indicator.
    """

    params = {
        # Standard MACD Parameters
        'macd1': 12, # moving average 1 length
        'macd2': 26, # moving average 2 length
        'macdsig': 9, # signal line moving average length
        'atrperiod': 14,  # ATR Period (standard)
        'atrdist': 3.0,   # ATR distance for stop price
        'smaperiod': 30,  # SMA Period (pretty standard)
        'dirperiod': 10  # Lookback period to consider SMA trend direction
    }

    def log(self, txt, dt=None):
        '''Logging function for strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        super(MACD_Crossover, self).__init__()

        # construct MACD indicator
        self.macd = bt.indicators.MACD(self.data,
                                        period_me1=self.p.macd1,
                                        period_me2=self.p.macd2,
                                        period_signal=self.p.macdsig)

        # Cross of MACD line and MACD signal line
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # set stop price indicator
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

    def add_data(cerebro):
        """Add data to backtrader cerebro - data class is created below"""
        data=MyFeed()
        cerebro.add_data(data)
        return data 

    def starting_cash(self):
        """set starting cash value"""
        self.val_start = self.broker.get_cash()

    def notify_order(self, order):
        """monitor order status and send order confirmation"""
        if order.status == order.Completed: # order is completed - nothing to do
            pass

        if not order.alive():
            # indicate no order is pending
            self.order = None
            
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker
            return
        
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]: # log buy and sell orders
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            # log cancelled orders
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        """Define MACD Strategy. next function is used for running strategies in backtrader cerebro"""
        self.log('Close, %.2f' % self.data.close[0]) # log the closing price of the series from the reference

        share_purchase = int(self.data.close / self.data.close) # calculate total shares you can purchase with total portfolio value
        
        if self.mcross == 1: # bullish MACD crossover
            self.order = self.buy(size = share_purchase) # execute buy order
            self.log('BUY CREATE, %.2f' % self.data.close[0]) # log buy order
        elif self.macd.signal > self.macd.signal:
            if not self.position:
                # rebuy MACD after crossover if parameters are true and if strategy sold stock midcrossover based on parameters below
                if self.macd.macd[0] - self.signal.signal[0] > self.macd.macd[-1] - self.macd.signal[-1]:
                    self.order = self.buy(size = share_purchase)
                    self.log('BUY CREATE, %.2f' % self.data.close[0])

        else:
            if self.macd.signal > self.macd.signal:
                if not self.position:
                    # sell based on crossover reversal
                    if self.macd.macd[0] - self.signal.signal[0] < self.macd.macd[-1] - self.macd.signal[-1]:
                        self.order = self.sell(size = share_purchase)
                        self.log('SELL CREATE, %.2f' % self.data.close[0])
            elif self.mcross == -1:
                self.order = self.sell(size = share_purchase) # sell at bearish crossover
                self.log('SELL CREATE, %.2f' % self.data.close[0]) # log sale

# class for loading 1 min interval dataset - written by Julian and editted by Angel
import pandas as pd
from backtrader.feed import DataBase
from backtrader import date2num
from backtrader import TimeFrame
os.chdir(r'C:/Users/angel/Documents/Documents/GitHub/Group-Project-Hill-Wiley-Gwinn/Data')
df = pd.read_csv('AAPL_1min.csv')
df['datetime'] = pd.to_datetime(df['datetime'])
class MyFeed(DataBase):
    def __init__(self):
        super(MyFeed, self).__init__()
        self.list = df # dataframe with date-time OHLC structure
        self.n = 0

        self.fromdate = self.list['datetime'][0] # 1st available date within data set
        self.todate = self.list['datetime'][len(self.list) - 1] # last available date within data set
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

        r = self.list.iloc[self.n]
        self.lines.datetime[0] = date2num(r['datetime'])

        self.lines.open[0] = r['open']
        self.lines.high[0] = r['high']
        self.lines.low[0] = r['low']
        self.lines.close[0] = r['close']
        self.lines.volume[0] = r['volume']
        self.m[r['datetime']] = r

        self.n = self.n + 1
        return True

if __name__ == '__main__':
    # instantiate cerebro class from backtrader
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(MACD_Crossover)

    # Create a Data Feed
    # os.chdir(r'C:/Users/angel/Documents/Documents/GitHub/Group-Project-Hill-Wiley-Gwinn/Data')
    # print(os.listdir())
    pricedata = bt.feeds.YahooFinanceCSVData(dataname='AAPL_1min.csv')

    data = MyFeed()

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set starting cash value
    cerebro.broker.setcash(2500)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)

    # Print out initial portfolio value
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run backtest
    cerebro.run()

    # Print out final portfolio value
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())