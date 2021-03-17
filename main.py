import random
import string
import time

import pyspark
from pyspark.context import SparkContext, SparkConf
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession
import re

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
spark = SparkSession(sc)

def cleanText(x):
    if x is None:
        return ''
    punc_cleanr = re.compile('&#39;|&#x27;')
    x2 = re.sub(punc_cleanr, '', str(x).lower())
    cleanr = re.compile('<.*?>|&([a-z0-9]+?|#[0-9]{1,6}|#x[0-9a-fA-F]{1,6});')
    x3 = re.sub(cleanr, ' ', x2)
    # Remove punctuation
    return x3.translate(str.maketrans('', '', string.punctuation.replace("'","")))


# Get dataFrame of file
df = spark.read.csv("/spring2021/project1/hacker_news_sample.csv", header=True, inferSchema=True)
# Convert to RDD and one list of cleaned words
rdd = df.rdd \
    .map(lambda x: x[2]) \
    .map(cleanText) \
    .flatMap(lambda x: x.split()) \
    .map(lambda x: (x, 1)) \
    .reduceByKey(lambda x,y: x+y)

values = rdd.collect()
values.sort(key= lambda x: x[1],reverse=True)
#[print(i) for i in values[0:10]]

sum([1 for i in values if i[1]==1])

