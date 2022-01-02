import models
import os
import sys
from datetime import datetime
import pandas as pd
import tensorflow as tf
import json
import numpy as np


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

def getFiles(paths: list[str]) -> list[str]:
    """File or folder paths are expected as arguments"""
    files = []
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            files += filesFromDir(dir=path)

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