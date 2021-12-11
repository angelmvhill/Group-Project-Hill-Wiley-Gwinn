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

import logging

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class Connection:
    """
    EMR Connection Handler
    """
    def __init__(self):
        """

        """

    def connect(self):
        """

        """
        spark = SparkSession\
            .builder\
            .appName("AlgoTradingETL")\
            .getOrCreate()

        self.spark = spark
        return spark
