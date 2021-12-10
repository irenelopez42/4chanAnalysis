"""
Created on Tue Nov 23 11:20:36 2021

@author: Irene Lopez

Collect older thread from 4plebs (maybe add more archives)
"""

import requests
import time

irrelevant_keys = ['doc_id', 'num', 'subnum', 'op', 'timestamp_expired', 'capcode', 'email',
                   'name', 'trip', 'poster_hash', 'poster_country', 'sticky', 'locked', 'deleted',
                   'nimages', 'fourchan_date', 'comment_sanitized', 'comment_processed', 'formatted',
                   'title_processed', 'name_processed', 'email_processed', 'trip_processed', 
                   'poster_hash_processed', 'poster_country_name', 'poster_country_name_processed', 
                   'exif', 'troll_country_code', 'troll_country_name', 'since4pass', 'unique_ips', 
                   'extra_data', 'media', 'board', 'nreplies']  # may be changed depending on needs

# user specific
headers = {'User-Agent': 'asfkhfbsdmn'}    

def mon_to_number(mon):
    """ takes month abbreviation and gives back number"""
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, 
                    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, 
                    "Oct": 10, "Nov": 11, "Dec": 12}
    return months[mon]

def search_4plebs(start_date, end_date, board):
    """ Search for posts in specific board, during specific timeframe in the 4plebs archive """
    
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
    
    for n in range(len(posts)):
        for key in irrelevant_keys:
            del posts[n][key]   # remove irrelevant entries
    
    return posts

def get_4plebs(board, thread_id):
    """ Look for specific thread in 4plebs archive. 
    Returns dict of info about original post and a list of comments """
    
    url = "http://archive.4plebs.org/_/api/chan/thread/?board={}&num={}".format(board, thread_id)
    
    # tries to access endpoint. If exception, wait 5 seconds and try again. Maximum 10 tries.
    for tries in range(10):
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        
            r = r.json()
            break
        except:
            time.sleep(5)
            
    keys = list(r['{}'.format(thread_id)].keys())
    
    original = r['{}'.format(thread_id)][keys[0]]
    
    for key in irrelevant_keys:
        del original[key]
    
    if len(keys) > 1:
        comments = r['{}'.format(thread_id)][keys[1]]
        comments_text = []
    
        for n in comments.keys():
            comment = comments[n]['comment']
            comments_text.append(comment)
    else:
        comments_text = []

    return original, comments_text
    

def main():
    """ Just a test on how this works. """
    
    board = 'pol'
    start_date = "2013-12-01"  # format YYYY-MM-DD
    end_date = "2014-12-01"
    
    posts = search_4plebs(start_date, end_date, board)
    
    print("Keys in post:", posts[0].keys())
    for n in range(len(posts)):
        print("Date of post {}:".format(n), time.ctime(posts[n]['timestamp']))
 
    thread_id = posts[0]['thread_num']
    thread, comments = get_4plebs(board, thread_id)
    print(thread)
    print(comments[0])
    
#    with open("test.json", 'w') as f:
#        json.dump(posts, f)
    

if __name__ == "__main__":
    main()
