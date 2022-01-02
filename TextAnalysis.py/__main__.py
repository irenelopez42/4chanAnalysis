import sys
import argparse
import chan_io as io
import chan_language as lang

def doTheMagic():
    """Load files from the cl arguments, extract posts and store as dataframe"""
    parser = argparse.ArgumentParser(prog= '4chan Text Analysis', description="A programm for extracting language features from 4chan threads")
    parser.add_argument('files', type=str, nargs='+', action='store', help='list of source files or directories containing the files')
    parser.add_argument('-o', type=str, action='store', nargs=1, help='The path for the output of the program')
    parser.add_argument('-v', nargs=1, action='store', type=str, help='The path to the vocabulary to be used')
    parser.add_argument('--count', action='store_true',help='If true, count the number of occurences of the words given in vocab')
    args = parser.parse_args(sys.argv)
    
    files = io.getFiles(args.files)
    posts = io.loadPosts(files)
    counts = lang.mapTokenCounts(posts, args.v, args.count)

    try:
        counts.to_pickle(args.o)
    except:
        print("Failed to store result in file")
        sys.exit(3)

if __name__ == '__main__':
    doTheMagic()