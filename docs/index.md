## OIM 3640 Problem Solving and Software Design Final Project 

Trading Bot Project:

Click here to see the [libraries we used](https://julianwileymac.github.io/Group-Project-Hill-Wiley-Gwinn/libraries)

## Project Summary and Goals

The goal of this project was to create a framework for developing, training, and backtesting algorithmic trading models. Although we created a strategy to backtest, the focus was not on the strategy itself, but rather the framework itself. THe strategy is replaceable, and the framework around the sample strategy we created is what will fuel our future algotrading strategy developments.

## User Instructions/README

For a usage summary and installation guide, see the [README file](https://github.com/angelmvhill/Group-Project-Hill-Wiley-Gwinn#readme).

## Project Evolution

At the beginning of this project, we were originally planning on using two small data sets from Yahoo Finance - a daily interval price data on Apple and a fundamentals dataset on Apple. However, these data sets only went back several years and were extremely small. We wanted to lean closer towards big data so that we could develop a better machine learning and data processing framework that was capable of processing much larger data sets. In attempt to obtain better resources, we applied to the Weissman Foundry Fellowship Program, and were accepted into the Fall 2021 cohort. We were granted $1000 for our project, which we used to purchase a historical data set from First Rate Data on 15-20 years of 1 minute interval price data on 3000 stocks. With this dataset, we were able to build a much more sophisticated framework that is much more scalable in terms of processing large data sets.

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

## EMR

![image](https://user-images.githubusercontent.com/77561896/145662715-e927ea50-31e0-42d9-b2d1-0a8610abd184.png)



## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/julianwileymac/Group-Project-Hill-Wiley-Gwinn/edit/main/docs/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/julianwileymac/Group-Project-Hill-Wiley-Gwinn/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.


