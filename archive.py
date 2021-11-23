"""
Created on Tue Nov 23 11:20:36 2021

@author: Irene Lopez

Collect older thread from 4plebs (maybe add more archives)
"""

import requests
import json
import time

def search_4plebs(start_date, end_date, board):
    """ Search for posts in specific board, during specific timeframe in the 4plebs archive """
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}    
    url = "http://archive.4plebs.org/_/api/chan/search/?boards={}&start={}&end={}&results=thread&order=asc".format(board, start_date, end_date)
    
    # tries to access endpoint. If exception, wait 5 seconds and try again. Maximum 10 tries.
    for tries in range(10):
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        
            r = r.json()
            break
        except:
            time.sleep(5)
        

    
    posts = r['0']['posts']  # get posts and ignore metadata
    
    irrelevant_keys = ['doc_id', 'num', 'subnum', 'op', 'timestamp_expired', 'capcode', 'email',
                       'name', 'trip', 'poster_hash', 'poster_country', 'sticky', 'locked', 'deleted',
                       'nimages', 'fourchan_date', 'comment_sanitized', 'comment_processed', 'formatted',
                       'title_processed', 'name_processed', 'email_processed', 'trip_processed', 
                       'poster_hash_processed', 'poster_country_name', 'poster_country_name_processed', 
                       'exif', 'troll_country_code', 'troll_country_name', 'since4pass', 'unique_ips', 
                       'extra_data', 'media', 'board']  # may be changed depending on needs
    
    for n in range(len(posts)):
        for key in irrelevant_keys:
            del posts[n][key]   # remove irrelevant entries
    
    return posts

def main():
    """ Just a test on how this works. """
    
    board = 'pol'
    start_date = "2013-12-01"  # format YYYY-MM-DD
    end_date = "2014-12-01"
    
    posts = search_4plebs(start_date, end_date, board)
    
    print("Keys in post:", posts[0].keys())
    for n in range(len(posts)):
        print("Date of post {}:".format(n), time.ctime(posts[n]['timestamp']))
 
    with open("test.json", 'w') as f:
        json.dump(posts, f)
    

if __name__ == "__main__":
    main()
