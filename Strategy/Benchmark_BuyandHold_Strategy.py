import backtrader as bt
import datetime
import os

class BuyandHold(bt.Strategy):
    """
    This class serves as the benchmark strategy, or buying and holding the traded asset.
    """

    def log(self, txt, dt=None):
        '''Logging function for strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def add_data(cerebro):
        data=MyFeed()
        cerebro.add_data(data)
        return data 

    def starting_cash(self):
        # set starting cash value
        self.val_start = self.broker.get_cash()
    
    def next(self):
        # Buy shares with all available cash
        num_of_shares = int(self.broker.get_cash() / self.data.close)
        
        if not self.position:
            self.buy(size = num_of_shares)
        if (len(self.datas) - len(self)) == 1:
            self.close()
    
    def log(self, txt, dt=None):
        '''Logging function for strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending
            
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker
            return
        
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def calc_roi(self):
        # calculate returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('ROI:                     {:.2f}%'.format(100.0 * self.roi))

# class for loading 1 min dataset - wrote by Julian
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
        self.list = df
        self.n = 0

        self.fromdate = self.list['datetime'][0]
        self.todate = self.list['datetime'][len(self.list) - 1]
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
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(BuyandHold)

    # Create a Data Feed 

    data = MyFeed()

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(2500)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run backtest
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())