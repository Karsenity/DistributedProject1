import re
import string
import nltk

"""
:param: list(string) <- single line
:return: list(list(string)) <- list of sentences
"""
def split_sentences(text):
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text.lower())
    return [sent.translate(str.maketrans('', '', string.punctuation.replace("'",""))) for sent in sentences]

"""
:param: list(string) <- a single sentence
:return: list((str,str))
"""
def tag_words(text):
    return nltk.pos_tag(text, tagset="universal")


"""
:param {(string,string) : int}
"""
def write_csv(results, filepath):
    import csv
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        [writer.writerow([key[0], key[1], results[key]]) for key in results]


"""
:param: ((string, string), int)
:returns: {(string,string) : int}
"""
def lemmatize_words(words):
    # Remove stopwords
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word[0][0] not in stop_words]

    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    word_dictionary = {}
    for word in words:
        lem_key = (lemmatizer.lemmatize(word[0][0]), word[0][1])
        if lem_key in word_dictionary:
            word_dictionary[lem_key]+=word[1]
        else:
            word_dictionary[lem_key]=word[1]
    return word_dictionary