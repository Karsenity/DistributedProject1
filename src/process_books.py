from processing.text_processing_functions import *

novel_filepaths = {
    "cities" : '/spring2021/project1/comparison/Charles Dickens - Cities.txt',
    "sherlock": '/spring2021/project1/comparison/Conan Doyle - Sherlock.txt',
    "moby": '/spring2021/project1/comparison/Herman Melville - Moby.txt',
    "pride": '/spring2021/project1/comparison/Jane Austen - Pride.txt',
    "frankenstein": '/spring2021/project1/comparison/Mary Shelley - Frankenstein.txt',
    "scarlet": '/spring2021/project1/comparison/Nathaniel Hawthorne - Scarlet.txt',
    "gatsby": '/spring2021/project1/comparison/Scott Fitzgerald - Gatsby.txt'
}


def process_novel(spark, novel):
    rdd = spark.sparkContext.textFile(novel_filepaths[novel])
    rdd = rdd \
        .flatMap(split_sentences) \
        .map(lambda x: x.split()) \
        .flatMap(tag_words) \
        .map(lambda x: (x,1)) \
        .reduceByKey(lambda x,y: x+y)
    return rdd.collect()


def get_novel_dfs(spark, override=False):
    from os import path
    import pandas as pd
    novels = {}
    for novel in novel_filepaths.keys():
        filepath = "./parsed_text/" + novel + "_wc.csv"
        if not path.exists(filepath) or override==True:
            results = process_novel(spark, novel)
            lemmatized_results = lemmatize_words(results)
            write_csv(lemmatized_results, filepath)
        novels[novel] = pd.read_csv(filepath, names=["Word", "POS", "Count"])
    return novels
