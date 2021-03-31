from processing.text_processing_functions import *


def clean_text(text):
    if text is None:
        return ''
    whitelist = set(string.ascii_lowercase + string.digits + string.punctuation + " ")
    x1 = ''.join(c for c in text.lower() if c in whitelist)
    x2 = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|\-)*\b', '', x1, flags=re.MULTILINE)
    regex = '\\S+@\\S+'
    x3 = re.sub(regex, '', x2)
    return x3.strip()

def process_blogtext(spark):
    df = spark.read.csv("/spring2021/project1/blogtext.csv", header=True, inferSchema=True)
    import random
    rdd = df.rdd \
        .map(lambda x: x[6]) \
        .map(clean_text) \
        .flatMap(split_sentences) \
        .map(lambda x: x.split()) \
        .flatMap(tag_words) \
        .map(lambda x: (x,1))
        #.reduceByKey(lambda x,y:x+y)
    return rdd



def get_blogtext_df(spark, override=False):
    from os import path
    import pandas as pd
    filepath = "./parsed_text/blogtext_wc.csv"
    if not path.exists(filepath) or override==True:
        results = process_blogtext(spark)
        write_csv(results, filepath, )
    df = pd.read_csv(filepath, names=["Word", "POS", "Count"])
    return df
