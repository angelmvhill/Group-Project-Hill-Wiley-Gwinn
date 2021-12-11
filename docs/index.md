## OIM 3640 Problem Solving and Software Design Final Project 

Click here to see the [libraries we used](https://julianwileymac.github.io/Group-Project-Hill-Wiley-Gwinn/libraries)

## Project Summary and Goals

The goal of this project was to create a framework for developing, training, and backtesting algorithmic trading models. Although we created a strategy to backtest, the focus was not on the strategy itself, but rather the framework itself. THe strategy is replaceable, and the framework around the sample strategy we created is what will fuel our future algotrading strategy developments.

## User Instructions/README

For a usage summary and installation guide, see the [README file](https://github.com/angelmvhill/Group-Project-Hill-Wiley-Gwinn#readme).

## Project Evolution

At the beginning of this project, we were originally planning on using two small data sets from Yahoo Finance - a daily interval price data on Apple and a fundamentals dataset on Apple. However, these data sets only went back several years and were extremely small. We wanted to lean closer towards big data so that we could develop a better machine learning and data processing framework that was capable of processing much larger data sets. In attempt to obtain better resources, we applied to the Weissman Foundry Fellowship Program, and were accepted into the Fall 2021 cohort. We were granted $1000 for our project, which we used to purchase a historical data set from First Rate Data on 15-20 years of 1 minute interval price data on 3000 stocks. With this dataset, we were able to build a much more sophisticated framework that is much more scalable in terms of processing large data sets. More specifically, this dataset was much too large to process using internal memory, so we had to process it across multiple machines. Therefore, we had to build a framework capable of processing a dataset this large, and we eliminated it from being an issue in the future given that we planned on using larger data sets.

## Strategy Performance

Compared to the benchmark strategy, the sample MACD strategy performed horribly. Despite the strategy losing money, this project is still a successful project. As mentioned before, the main goal of this project was to develop a framework for developing trading algorithms, rather than developing a successful trading algorithm. The framework is more important than the strategy itself because it is what allows it to be successful. Without a robust development framework for the strategy, a myraid of issues can occur.

To name a few:
- incorrect backtesting output, resulting in deploying an unprofitable strategy
- latencies when sending orders resulting in orders being sent late or not being 
- logging orders incorrectly, resulting in showing profits when in reality we are losing money

For this reason, it is not yet necessary to develop a profitable strategy, but rather it is more important that our framework was airtight. Given the time available to build out this programt, we created a framework that was a robust as possible.

Nevertheless, here are the outputs and backtesting results of the strategy.

**Note: Both portfolios started at $2500 USD.**

Benchmark Strategy Results:

![image](https://user-images.githubusercontent.com/77561896/145662442-9603bab9-e3ed-45a3-af73-13024eb07b97.png)

MACD Strategy Results:

![image](https://user-images.githubusercontent.com/77561896/145663200-c78c9712-7ed4-4afa-8c9b-01f02d36db28.png)

## Notebook Output for Inputting Data into EMR

Although this isn't much to look at, we have too much data to create a visual output without spending too much money (the data set is 100 GB). This is the first 20 rows of a Spark dataframe, which is qthe equivalent to a pandas dataframe in Spark. The main difference is that this dataframe is representational, meaning that it tells the machine where the data is stored, rather than actually importing it into memory. With the knowledge of this location, the machine can querie the data when needed.

![image](https://user-images.githubusercontent.com/77561896/145662715-e927ea50-31e0-42d9-b2d1-0a8610abd184.png)

To learn more about Spark dataframes, click [here](https://spark.apache.org/docs/latest/sql-programming-guide.html).

## Summary

Overall, this project was very successful. We accomplished a lot of goals and were able to establish a solid framework that we are excited to continue building off of in the future.
