"""
Created on Sun Jan 23 14:47:47 2022

@author: Irene

From counts of hate speech words, create histogram of evolution
"""

import pandas as pd
import matplotlib.pyplot as plt
    

def main():
    
    fig, axes = plt.subplots(nrows=1, ncols=3)
    
    for i, board in enumerate(['sci', 'news', 'adv']):
        
        # load file
        df = pd.read_csv(f"Counts/{board}_counts.csv")
        
        # remove post if no hate words
        df = df.dropna(how='any', axis=0)
        
        # matched vocabulary into a list
        df['matched_vocab'] = df.matched_vocab.apply(lambda x: x.split(','))
        
        # add column with length of that list
        df['length'] = df.matched_vocab.str.len()
        
        # change unix timestamp to pandas readable date and add column for month
        df['date'] = pd.to_datetime(df.timestamp, unit='s')
        df['month'] = pd.to_datetime(df.date).dt.to_period('M')
        
        # group post by month and plot histogram
        df.groupby('month')['length'].count().plot.bar(ax=axes[i])
            

    
    return

if __name__ == '__main__':
    main()