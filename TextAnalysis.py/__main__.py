import sys
import argparse

import chan_io as io
import chan_language as lang
import os
import numpy as np

def doTheMagic():
    """Load files from the cl arguments, extract posts and store as dataframe"""
    parser = argparse.ArgumentParser(prog= '4chan Text Analysis', description="A programm for extracting language features from 4chan threads")
    parser.add_argument('files', type=str, nargs='+', action='store', help='list of source files or directories containing the files')
    parser.add_argument('-o', type=str, action='store', nargs=1, help='The path for the output of the program. Word counts are stored as csv. The vocab as pickle file')
    parser.add_argument('-v', nargs=1, action='store', type=str, help='The path to the vocabulary to be used')
    parser.add_argument('--extract_vocab', action='store_true',help='If true, expect the path to the vocabulary json as first argument and extract the vocab into a numpy array and store it at the -o path')
    args = parser.parse_args(sys.argv)

    if args.extract_vocab:
        print("Extracting vocabulary into numpy binary")
        vocab = io.extractVocab(args.files[1])
        with open(args.o[0], 'wb') as file:
            np.save(file,vocab)
    else:
        files = io.getFiles(args.files[1:])
        with open(args.v[0], 'rb') as file:
                vocab = np.load(file)
        print("Extract vocabulary matches for files:")
        print(files)
        df = io.loadPostsFromJson(files)
        df.loc[:,"matched_vocab"] = lang.mapTokenCounts(df.loc[:,"content"].to_numpy(),vocab)
        df.to_csv(args.o[0])
        
if __name__ == '__main__':
    doTheMagic()