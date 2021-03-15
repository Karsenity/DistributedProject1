import random

import pyspark
from pyspark.context import SparkContext, SparkConf
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
spark = SparkSession(sc)


data = [random.randint(20) for i in range(10000)]

my_rdd = sc.parallelize(data)

def nothing(x):
    return x

def average(x, y):
    return (x+y)/2

mapped_rdd = my_rdd.map(nothing)

reduced_rdd = mapped_rdd.reduce(average)






# rdd=sc.textFile("/team/blogtext.csv")
#
# mappedRdd= rdd.map(lambda x:x.split(","))
# pairs = mappedRdd.map(lambda s: (s, 1))