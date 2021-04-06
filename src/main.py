from pyspark.context import SparkContext
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession
import pandas as pd

from process_HackerNews import get_hacker_df
from process_blogtext import get_blogtext_df
from process_books import get_novel_dfs
import matplotlib.pyplot as plt
# sc = SparkContext.getOrCreate()
# sqlContext = SQLContext(sc)
# spark = SparkSession(sc)



novels = get_novel_dfs("spark")
blog_text = get_blogtext_df("spark")
hacker_news = get_hacker_df("spark")
# print(hacker_news.head())
#
# """
# Example of getting word-counts from DF"""
# df = hacker_news.groupby(["Word"]).sum()
# df = df.sort_values(["Count"], ascending=False)
# print(df.head())
#
# """
# Example of getting just one type of tag from DF"""
# df = hacker_news[hacker_news["POS"].isin(["JJ","JJR","JJS"])]
# df = df.sort_values(["Count"], ascending=False)
# print(df.head())

"""
Combining blog_posts and hacker_news into one dataset called new_text"""
new_text = pd.concat([hacker_news, blog_text]).groupby(["Word", "POS"], as_index=False).sum()
"""
Combining all the novels into one dataframe called formal_text"""
formal_text = pd.DataFrame({"Word":[], "POS":[], "Count":[]})
for novel in novels.keys():
    formal_text = pd.concat([novels[novel], formal_text])
formal_text = formal_text.groupby(["Word", "POS"], as_index=False).sum()

"""
list of just adjectives from formal_text and new_text"""
new_adj = new_text[new_text["POS"].isin(["JJ","JJR","JJS"])]
formal_adj = formal_text[formal_text["POS"].isin(["JJ","JJR","JJS"])]

new_adj = new_adj.sort_values(["Count"], ascending=False)
formal_adj = formal_adj.sort_values(["Count"], ascending=False)

print(new_adj.head())
print(formal_adj.head())

pd.options.plotting.backend = "plotly"
fig = new_adj.head(10).plot.bar(x="Word", y="Count")
fig.show()
#plt.show()
# df = df.sort_values(by=['Count'], ascending=False)
# values = df.values.tolist()












