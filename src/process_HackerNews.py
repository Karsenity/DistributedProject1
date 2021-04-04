import re
import string


"""
This function removes improper HTML tags that were carried over with the file
"""
def cleanText(x):
    if x is None:
        return ''
    punc_cleanr = re.compile('&#39;|&#x27;')
    x2 = re.sub(punc_cleanr, '', str(x).lower())
    cleanr = re.compile('<.*?>|&([a-z0-9]+?|#[0-9]{1,6}|#x[0-9a-fA-F]{1,6});')
    x3 = re.sub(cleanr, ' ', x2)
    return x3

def split_sentences(text):
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text)
    return [sent.translate(str.maketrans('', '', string.punctuation.replace("'",""))) for sent in sentences]

def tag_words(text):
    import nltk

    return nltk.pos_tag(text)

def lemmatize_words(words):
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [((lemmatizer.lemmatize(word[0][0]), word[0][1]), word[1]) for word in words]
    fix_count =


def process_hackerNews(spark):
    # Get dataFrame of file
    df = spark.read.csv("/spring2021/project1/hacker_news_sample.csv", header=True, inferSchema=True)
    # Convert to RDD and one list of cleaned words
    rdd = df.rdd \
        .map(lambda x: x[2]) \
        .map(cleanText) \
        .flatMap(split_sentences) \
        .map(lambda x: x.split()) \
        .flatMap(tag_words) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(lambda x,y: x+y)
    return rdd.collect()


def write_csv(results):
    import csv
    with open("./parsed_text/hacker_news_wc.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        [writer.writerow([row[0][0], row[0][1], row[1]]) for row in results]


"""
Function you should be calling to get a cleaned and tagged dataframe of 
words from the hacker_news dataset. set override=True if you want to remake
the csv-results.
"""
def get_hacker_df(spark, override=False):
    from os import path
    import pandas as pd
    filepath = "./parsed_text/hacker_news_wc.csv"
    if not path.exists(filepath) or override==True:
        results = process_hackerNews(spark)
        write_csv(results)
    df = pd.read_csv(filepath, names=["Word", "POS", "Count"])
    return df
