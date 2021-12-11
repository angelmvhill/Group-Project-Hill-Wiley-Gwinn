## OIM 3640 Problem Solving and Software Design Final Project 

Trading Bot Project:

Click here to see the [libraries we used](https://julianwileymac.github.io/Group-Project-Hill-Wiley-Gwinn/libraries)

## Project Summary and Goals

The goal of this project was to create a framework for developing, training, and backtesting algorithmic trading models. Although we created a strategy to backtest, the focus was not on the strategy itself, but rather the framework itself. THe strategy is replaceable, and the framework around the sample strategy we created is what will fuel our future algotrading strategy developments.

## User Instructions/README

For a usage summary and installation guide, see the [README file](https://github.com/angelmvhill/Group-Project-Hill-Wiley-Gwinn#readme).

## Strategy Performance

Compared to the benchmark strategy, the sample MACD strategy performed horribly. Despite the strategy losing money, this project is still a successful project. As mentioned before, the main goal of this project was to develop a framework for developing trading algorithms, rather than developing a successful trading algorithm. The framework is more important than the strategy itself because it is what allows it to be successful. Without a robust development framework for the strategy, a myraid of issues can occur.

To name a few:
- incorrect backtesting output, resulting in deploying an unprofitable strategy
- latencies when sending orders resulting in orders being sent late or not being 
- logging orders incorrectly, resulting in showing profits when in reality we are losing money

For this reason, it is not yet necessary to develop a profitable strategy, but rather it is more important that our framework was airtight. Given the time available to build out this programt, we created a framework that was a robust as possible.

Nevertheless, here are the outputs and backtesting results of the strategy.

Note: Both portfolios started at $2500 USD.

Benchmark Strategy Results:

![image](https://user-images.githubusercontent.com/77561896/145662442-9603bab9-e3ed-45a3-af73-13024eb07b97.png)

MACD Strategy Results:



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


