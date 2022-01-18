import nltk
from tensorflow import keras
from tensorflow import strings
import tensorflow as tf
import re, string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def removeDuplicateTokens(text):
    return " ".join(set(word_tokenize(text.numpy().decode('utf-8'))))

def vectorizeLayer(vocab: np.ndarray) -> tf.Tensor:
    """
    Create a tensor for text vectorization based on the given vocabulary as a numpy array.
    If multi_hot = False, count of vocab occurrences is ignored.
    See the documentation on keras' TextVectorization layer for more
    """
    return keras.layers.TextVectorization(
        standardize=None,
        output_mode='multi_hot',
        vocabulary = vocab
    )

def mapTokenCounts(text: str, vocab: np.ndarray) -> str:
    """
    map the given post to matched words from the vocabulary
    """
    vector_layer = vectorizeLayer(vocab)
    t = tf.constant(text)
    counts = vector_layer(t).numpy()[1:]
    counts = counts.astype(np.bool8)
    return " ".join(vocab[counts])
    

def standardizer(text: str) -> str:
    """A method for standardizing a given string tensor"""
    lowercased = text.lower()
    html_stripped = strings.regex_replace(lowercased, "<[^>]+>", " ")
    punctuation_stripped = strings.regex_replace(html_stripped, "[%s]" % re.escape(string.punctuation), "").numpy().decode('utf-8')
    lemmatizer = WordNetLemmatizer()
    lemmatized = " ".join(map(lemmatizer.lemmatize, word_tokenize(punctuation_stripped)))
    return lemmatized
