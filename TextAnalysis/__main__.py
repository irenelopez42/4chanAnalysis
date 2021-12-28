from genericpath import isfile
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
import sys
import os
import argparse

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def filesFromDir(dir: str, files: list[str] = None) -> list[str]:
    """Return a recursively build list of all files that can be found in a directory and its subdirectories"""
    if files is None:
        files = []

    if not os.path.isdir(dir):
        return files
    
    for file in filter(os.path.isfile, os.listdir(dir)):
        files.append(file)
    for dir in filter(os.path.isdir, os.listdir(dir)):
        files += filesFromDir(dir, files)

    return files

def getFiles(*args) -> list[str]:
    """File or folder paths are expected as arguments"""
    files = []
    for arg in args:
        if os.path.isfile(arg):
            files.append(files)
        elif os.path.isdir(arg):
            files += filesFromDir(dir=arg)

    if len(files) == 0:
        print("Failed to find any input files")
        sys.exit(1)

    return files

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

    if len(posts) == 0:
        print("No posts could be extracted")
        sys.exit(2)
    
    return posts

def makeDataset(inputs: np.ndarray) -> tf.data.Dataset:
    return tf.data.Dataset.from_tensor_slices(inputs)

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

def mapTokenCounts(posts: list[tuple[int,datetime,str]], vocab: np.ndarray, counts = False) -> pd.DataFrame:
    """
    map the given posts to their respective vocab counts and return a pandas DataFrame containing the word counts as numpy arrays
    """
    df = makePandas(posts)
    data = makeDataset(df.loc[:,'text'])
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

def doTheMagic():
    """Load files from the cl arguments, extract posts, """
    parser = argparse.ArgumentParser(prog= '4chan Text Analysis', description="A programm for extracting language features from 4chan threads")
    parser.add_argument('files', type=str, nargs='+', action='store', help='list of source files or directories containing the files')
    parser.add_argument('-o', type=str, action='store', nargs=1, help='The path for the output of the program')
    parser.add_argument('-v', nargs=1, action='store', type=str, help='The path to the vocabulary to be used')
    parser.add_argument('--count', action='store_true',help='If true, count the number of occurences of the words given in vocab')
    args = parser.parse_args(sys.argv)
    
    files = getFiles(*args.files)
    posts = loadPosts(files)
    counts = mapTokenCounts(posts, args.v, args.count)

    try:
        counts.to_pickle(args.o)
    except:
        print("Failed to store result in file")
        sys.exit(3)

if __name__ == '__main__':
    doTheMagic()