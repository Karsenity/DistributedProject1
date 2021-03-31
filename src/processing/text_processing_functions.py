import re
import string


def split_sentences(text):
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text)
    return [sent.translate(str.maketrans('', '', string.punctuation.replace("'",""))) for sent in sentences]

def tag_words(text):
    import nltk
    tagged_words = nltk.pos_tag(text)
    return text


def write_csv(results, filepath):
    import csv
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        [writer.writerow([row[0][0], row[0][1], row[1]]) for row in results]