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
        'macd1': 12,
        'macd2': 26,
        'macdsig': 9,
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

    def starting_cash(self):
        # set starting cash value
        self.val_start = self.broker.get_cash()

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

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.data.close[0])

        share_purchase = int(self.data.close / self.data.close)
        
        if not self.position:
            if self.mcross == 1:
                self.order = self.buy(size = share_purchase)
                self.log('BUY CREATE, %.2f' % self.data.close[0])
            
        else:
            if self.mcross == -1:
                self.order = self.sell(size = share_purchase)
                self.log('SELL CREATE, %.2f' % self.data.close[0])

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(MACD_Crossover)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, r'C:\Users\angel\Documents\Documents\GitHub\Group-Project-Hill-Wiley-Gwinn\Data')
    os.chdir(r'C:/Users/angel/Documents/Documents/GitHub/Group-Project-Hill-Wiley-Gwinn/Data')
    print(os.listdir())
    # Create a Data Feed
    pricedata = bt.feeds.YahooFinanceCSVData(dataname='AAPL.csv')

    # Add the Data Feed to Cerebro
    cerebro.adddata(pricedata)

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