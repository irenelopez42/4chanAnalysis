import nltk
import models
from tensorflow import keras
from tensorflow import strings
import tensorflow as tf
import re, string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from datetime import datetime
import json
import numpy as np
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def loadPosts(files: list[str]) -> list[tuple[int,datetime,str]]:
    """Load all json files from the given list of files and convert them to posts"""
    posts = []
    for f in files:
        with open(f) as file:
            try:
                threads_json = json.load(file)
                for t in models.ChanThread.parseThreads(threads_json):
                    posts += t.asRawStrings()

            except:
                print(f"Could not read from file {f}")
                continue
    
    return posts

def makeDataset(inputs: np.ndarray) -> tf.data.Dataset:
    return tf.data.Dataset.from_tensor_slices(inputs).batch(64)

def makePandas(posts: list[tuple[int,datetime,str]]):
    columns = ["id","date","text"]
    return pd.DataFrame.from_records(posts, columns=columns)

def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    return " ".join(map(lemmatizer.lemmatize, word_tokenize(text.numpy().decode('utf-8'))))

def removeStopwords(text):
    words = stopwords.words('english')
    return " ".join(filter(lambda x: x not in words, word_tokenize(text.numpy().decode('utf-8'))))

def removeDuplicateTokens(text):
    return " ".join(set(word_tokenize(text.numpy().decode('utf-8'))))

def standardizer(input: tf.Tensor):
    """A method for standardizing a given string tensor"""
    lowercased = strings.lower(input)
    html_stripped = strings.regex_replace(lowercased, "<[^>]+>", " ")
    punctuation_stripped = strings.regex_replace(html_stripped, "[%s]" % re.escape(string.punctuation), "")
    stopwords_stripped = tf.py_function(removeStopwords,[punctuation_stripped],tf.string)
    lemmatized = tf.py_function(lemmatize,[stopwords_stripped],tf.string)

    return lemmatized

def standardize(text) -> str:
    return standardizer(text).numpy().decode('utf-8')

def vectorize_layer(vocab: np.ndarray, standardize_method=standardizer, multi_hot = False) -> tf.Tensor:
    """
    Create a tensor for text vectorization based on the given vocabulary as a numpy array.
    If multi_hot = True, count of vocab occurrences is ignored.
    See the documentation on keras' TextVectorization layer for more
    """
    return keras.layers.TextVectorization(
        standardize=standardize_method,
        output_mode='multi_hot' if multi_hot else 'count',
        vocabulary = vocab
    )

def mapTokenCounts(data:tf.data.Dataset, vocab: np.ndarray, counts = False):
    """
    map the given dataset to their respective vocab counts
    """
    layer = vectorize_layer(vocab, multi_hot=counts)
    return data.map(lambda x: layer(x))