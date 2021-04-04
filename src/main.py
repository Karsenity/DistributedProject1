import os
import random

import pyspark
from pyspark.context import SparkContext, SparkConf
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession
from nltk import pos_tag
import nltk
import time

from process_HackerNews import get_hacker_df

#os.chdir("./Project1/src")   #Do not remove: paramiko infers the wrong working directory otherwise
from process_blogtext import process_blogtext

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
spark = SparkSession(sc)


df = get_hacker_df(spark)


# print("\n\nTEST\n\n")
# start = time.perf_counter()
# values = process_blogtext(spark)
# test = values.take(3)
# print("Time elapsed: %s"%(time.perf_counter()-start))
# [print(i) for i in test]








