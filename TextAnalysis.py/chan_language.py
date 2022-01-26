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

def mapTokenCounts(text: np.ndarray, vocab: np.ndarray) -> np.ndarray:
    """
    map the given texts to matched words from the vocabulary
    """
    dset = tf.data.Dataset.from_tensor_slices(text)
    vector_layer = vectorizeLayer(vocab)
    dset = dset.map(lambda x: tf.expand_dims(x,-1)).map(vector_layer)
    return np.array(list(map(lambda x: " ".join(vocab[x[0][1:].astype(np.bool8)]), dset.as_numpy_iterator())))
    

def standardizer(text: str) -> str:
    """A method for standardizing a given string tensor"""
    lowercased = text.lower()
    html_stripped = strings.regex_replace(lowercased, "<[^>]+>", " ")
    number_stripped = strings.regex_replace(html_stripped, "[0-9]+", "")
    punctuation_stripped = strings.regex_replace(number_stripped, "[%s]" % re.escape(string.punctuation), "").numpy().decode('utf-8')
    lemmatizer = WordNetLemmatizer()
    lemmatized = " ".join(map(lemmatizer.lemmatize, word_tokenize(punctuation_stripped)))
    return lemmatized
