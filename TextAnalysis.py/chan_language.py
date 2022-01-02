import nltk
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
import sys
import chan_io as io

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

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

def mapTokenCounts(posts: list[tuple[int,datetime,str]], vocab: np.ndarray, counts = False) -> pd.DataFrame:
    """
    map the given posts to their respective vocab counts and return a pandas DataFrame containing the word counts as numpy arrays
    """
    df = io.makePandas(posts)
    data = io.makeDataset(df.loc[:,'text'])
    df = df.drop("text", axis=1)
    layer = vectorize_layer(vocab, multi_hot=counts)
    data = data.map(lambda x: layer(x)).as_numpy_iterator()
    df.loc[:,'word_count'] = np.array(data)
    
    return df

def extractVocab(file) -> np.ndarray:
    """Extact the vocabulary used for token count from the given file"""
    try:
        with open(file) as f:
            json_dict = json.load(f)
            vocab = map(lambda x: x['term'], json_dict)
    except:
        print("Could not read vocab json")
        sys.exit(3)

    lemmatizer = WordNetLemmatizer()
    vocab = list(map(lambda x: lemmatizer.lemmatize(x.lower()), vocab))
    return np.array(vocab)