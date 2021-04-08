from pyspark.context import SparkContext
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession
import pandas as pd

from process_HackerNews import get_hacker_df
from process_blogtext import get_blogtext_df
from process_books import get_novel_dfs
import matplotlib.pyplot as plt

from processing.plotting_code import *

"""sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
spark = SparkSession(sc)"""

novels = get_novel_dfs("spark")
blog_text = get_blogtext_df("spark")
hacker_news = get_hacker_df("spark")


"""
Combining blog_posts and hacker_news into one dataset called new_text"""
new_text = pd.concat([hacker_news, blog_text]).groupby(["Word", "POS"], as_index=False).sum()
"""
Combining all the novels into one dataframe called formal_text"""
formal_text = pd.DataFrame({"Word":[], "POS":[], "Count":[]})
for novel in novels.keys():
    formal_text = pd.concat([novels[novel], formal_text])
formal_text = formal_text.groupby(["Word", "POS"], as_index=False).sum()

# """
# list of just adjectives from formal_text and new_text"""
# new_adj = new_text[new_text["POS"].isin(["JJ","JJR","JJS"])]
# formal_adj = formal_text[formal_text["POS"].isin(["JJ","JJR","JJS"])]
#
# new_adj = new_adj.sort_values(["Count"], ascending=False)
# formal_adj = formal_adj.sort_values(["Count"], ascending=False)
# """
# Scale adjective datasets based on total number of adjectives"""
# modern_adj_total = new_adj["Count"].sum()
# new_adj["Count"] = new_adj["Count"].apply(lambda x: x/modern_adj_total*100)
# formal_adj_total = formal_adj["Count"].sum()
# formal_adj["Count"] = formal_adj["Count"].apply(lambda x: x/formal_adj_total*100)
# top_adj(new_adj, formal_adj)
# """
# Direct comparison of proportion of total words from modern vs formal that are adjectives"""
# modern_word_total = new_text["Count"].sum()
# formal_word_total = formal_text["Count"].sum()
# modern_prop = modern_adj_total / modern_word_total * 100
# formal_prop = formal_adj_total / formal_word_total * 100
# prop_adjectives(formal_prop, modern_prop)

"""
Treemap showing the division of each text based on proportion of words belong to each POS"""
pos_props(new_text, formal_text)

# plt.show()
# df = df.sort_values(by=['Count'], ascending=False)
# values = df.values.tolist()











