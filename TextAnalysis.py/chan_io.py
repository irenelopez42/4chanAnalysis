import chan_language as lang
import os
import sys
from datetime import datetime
import pandas as pd
import tensorflow as tf
import json
import numpy as np
from nltk.stem import WordNetLemmatizer


def filesFromDir(dir: str, files: list[str] = None) -> list[str]:
    """Return a recursively build list of all files that can be found in a directory and its subdirectories"""
    if files is None:
        files = []

    if os.path.isfile(dir):
        return files
    
    for file in filter(os.path.isfile, map(lambda x: dir + "/" + x, os.listdir(dir))):
        files.append(file)
    for dir in filter(os.path.isdir, map(lambda x: dir + "/" + x, os.listdir(dir))):
        files += filesFromDir(dir, files)

    return files

def getFiles(paths: list[str]) -> list[str]:
    """File or folder paths are expected as arguments"""
    files = []
    for path in paths:
        if os.path.isfile(path) and path.endswith(".json"):
            files.append(path)
        elif os.path.isdir(path):
            files += filesFromDir(dir=path)

    if len(files) == 0:
        print("Failed to find any input files")
        sys.exit(1)

    return files

def extractVocab(file) -> np.ndarray:
    """Extact the vocabulary used for token count from the given file"""
    vocab = []
    try:
        with open(file) as f:
            json_dict = json.load(f)
            for l in json_dict:
                vocab += map(lambda x: x['term'], l)
    except Exception as e:
        print("Could not read vocab json")
        print(e)
        sys.exit(3)

    vocab = list(map(lang.standardizer, vocab))

    return np.unique(vocab)

def parseOp(jsonPost):
    """Convert from json original post to timestamp, text tuple"""
    title = "" if jsonPost['title'] is None else jsonPost['title']
    comment = "" if jsonPost['comment'] is None else jsonPost['comment']
    return [int(jsonPost["timestamp"]), " ".join([title, comment])]

def parseThread(base_id, jsonThread):
    """Convert from json to pandas dataframe with columns timestamp and content and index of ids"""
    df = pd.DataFrame(columns=["timestamp","content"], index=pd.Index([],dtype=int, name="id"))
    id = base_id * 100
    op = parseOp(jsonThread["op"])
    df.loc[id] = op
    for p in jsonThread["replies"]:
        id += 1
        df.loc[id] = [op[0],p]

    return df

def loadPostsFromJson(paths: list[str]):
    """Extract all posts from the given json files, standardize the text and return a combined dataframe object"""
    files = getFiles(paths)
    df_posts = pd.DataFrame(columns=["timestamp","content"], index=pd.Index([],dtype=int, name="id"))

    for f in files:
        with open(f) as file:
            try:
                threads_json = json.load(file)
            except Exception as e:
                print(f"Could not read json file for threads: {e}")
            
            try:
                for t in threads_json.items():
                    df_posts = df_posts.append(parseThread(int(t[0]), t[1]))
            except Exception as e:
                print(f"Malformed json objects: {e}")

    df_posts = df_posts.dropna()

    df_posts.loc[:,"content"] = df_posts.loc[:,"content"].map(lang.standardizer)

    return df_posts