# Group-Project-Hill-Wiley-Gwinn

## Project Summary

This project contains 3 main parts: an algorithmic trading strategy framework, a data processing framework, and a machine learning framework. To run this code, you will need to install [the following packages](https://julianwileymac.github.io/Group-Project-Hill-Wiley-Gwinn/libraries).

The goal of this project was to create a framework for developing, training, and backtesting algorithmic trading models. Although we created a strategy to backtest, the focus was not on the strategy itself, but rather the framework itself. THe strategy is replaceable, and the framework around the sample strategy we created is what will fuel our future algotrading strategy developments.

## Algotrading Strategy Framework

We wrote code for 2 different algotrading strategies, one to serve as a template to develop further strategies and another to use as a benchhmark. The benchmark simply buys a share of stock at the beginning of the dataframe and sells it when the last record is passed through the backtesting engine cerebro. For this project, we used the MACD strategy as a placefiller strategy to ensure that our framework was functional, so in order to create another strategy, you simply need to change 3 things within the code for the MACD strategy: the params dictionary, the class __init__ constructor, and the code within the next function. These 3 things define the strategy, and the other code deals with data feeds, instantiating cerebro, and monitoring order status and trades. If you want to use a different dataset, simply change the file name in the code. However, you may need to manipulate some of the code if the data is in a format that backtrader does not recognize.

## Data Processing Framework



## Machine Learning Framework

