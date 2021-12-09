import backtrader as bt
from datetime import datetime
import os

class BuyandHold(bt.Strategy):

    def starting_cash(self):
        #set starting cash value
        self.val_start = self.broker.get_cash()

    def purchase_shares(self):
        # Buy shares with all available cash
        num_of_shares = int(self.broker.get_cash() / self.data.close)
        self.buy(size = num_of_shares) 

    def calc_roi(self):
        # calculate returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('ROI:                     {:.2f}%'.format(100.0 * self.roi))

os.chdir(r'C:/Users/angel/Documents/Documents/GitHub/Group-Project-Hill-Wiley-Gwinn/Data')
data = bt.feeds.YahooFinanceData(dataname="AAPL_1min.csv")

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(BuyandHold)
cerebro.broker.setcash(2500)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())