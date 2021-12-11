# Group-Project-Hill-Wiley-Gwinn

## Project Summary

This project contains 3 main parts: an algorithmic trading strategy framework, a data processing framework, and a machine learning framework. To run this code, you will need to install [the following packages](https://julianwileymac.github.io/Group-Project-Hill-Wiley-Gwinn/libraries).

The goal of this project was to create a framework for developing, training, and backtesting algorithmic trading models. Although we created a strategy to backtest, the focus was not on the strategy itself, but rather the framework itself. THe strategy is replaceable, and the framework around the sample strategy we created is what will fuel our future algotrading strategy developments.

To see the see our full project website in Github pages, click this [link](https://angelmvhill.github.io/Group-Project-Hill-Wiley-Gwinn/)

## Algotrading Strategy Framework

We wrote code for 2 different algotrading strategies, one to serve as a template to develop further strategies and another to use as a benchhmark. The benchmark simply buys a share of stock at the beginning of the dataframe and sells it when the last record is passed through the backtesting engine cerebro. For this project, we used the MACD strategy as a placefiller strategy to ensure that our framework was functional, so in order to create another strategy, you simply need to change 3 things within the code for the MACD strategy: the params dictionary, the class __init__ constructor, and the code within the next function. These 3 things define the strategy, and the other code deals with data feeds, instantiating cerebro, and monitoring order status and trades. If you want to use a different dataset, simply change the file name in the code. However, you may need to manipulate some of the code if the data is in a format that backtrader does not recognize.

## Data Processing Framework
Because we had a huge amount of data that was stored across multiple buckets in several different formats, we had to create a framework for ingesting, processing, and storing the data. Overall, we have about 2-3 Tb of data in the form of intraday pricing data, company fundamentals information, and various financial information on firms and industries. To deal wth this challenge, we chose to use Apache Spark via AWS EMR. Spark is a big data processing framework that uses distributed storage and processing technologies to work with datasets and is scalable up to petabytes of data. AWS EMR is Amazon's proprietary version of Apache Spark and is designed for big data engineering. EMR stands for Elastic Map Reduce, and it's named after the process by which EMR runs functions across the dataset.

## Machine Learning Framework
We created a machine learning framework to enable us to create and train machine learning strategies with our data processing framework. Because data is integral to machine learning, this framework was intimately connected to the data processing framework. We first had to select the machine learning libraries that we wanted to use because there are many python libraries for defining and training models. In the ends, we decided to use FinRL because it was specifically designed to work with stock data and has functionality that endable it to integrate with the trading/brokerage APIs like Alpaca, TD Ameritrade, and Polygon. Next, we transformed the data into a more machine learning friendly file format, specfically parquet, which enabled us to import the data into EMR. Next, we had to solve several package problems on EMR. Beacuase Apache Spark runs code across multiple machines, managing packages becomes difficult, especially when each machine has more than one python installation, and sometimes more than one pyhton kernel.
