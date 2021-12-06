#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:37:32 2021

@author: Irene Lopez Gutierrez

Collect random posts through time using the 4plebs API. Works for two boards: 'pol' and 'adv'.
"""

import sys
import requests
import json
import time
import numpy as np
from subprocess import call
from socket import gethostname
from archive import get_4plebs

# user specific
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}   

def main(board):
    
    # create empty dictionary with entries for each month of archive content
    dict_ids = {}
    
    if board == 'pol':
    
        dict_ids["2013"] = {"Nov": [], "Dec": []}
        
        for year in range(2014, 2022):
            dict_ids[ f"{year}" ] = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], 
                    "May": [], "Jun": [], "Jul": [], "Aug": [], "Sep": [], 
                    "Oct": [], "Nov": [], "Dec": []}   
            
        # create empty dict for each year
        years = [{}, {}, {}, {}, {}, {}, {}, {}, {}]
            
        # some info about the 4Plebs archive for /pol/
        init_year = 2013
        total_pages = 821178
        skip_pages = 266
        post_per_page = 10
        
        
    elif board == 'adv':
        
        for year in range(2014, 2022):
            dict_ids[ f"{year}" ] = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], 
                    "May": [], "Jun": [], "Jul": [], "Aug": [], "Sep": [], 
                    "Oct": [], "Nov": [], "Dec": []}
        
        # create empty dict for each year
        years = [{}, {}, {}, {}, {}, {}, {}, {}]
            
        # some info about the 4Plebs archive for /adv/
        init_year = 2014
        total_pages = 86415
        skip_pages = 30
        post_per_page = 10
        
    else:
        sys.exit("This board is not supported")

    
    for pag in range(1, total_pages + 1, 1 + skip_pages):
        
        url = f"http://archive.4plebs.org/_/api/chan/index/?board={board}&page={pag}&order=by_thread"

        # tries to acces url. If access denied, sleep 5 seconds. Maximum tries = 100
        for tries in range(100):
            try:
                r = requests.get(url, headers=headers)
                r.raise_for_status()
                r = r.json()
                break
                    
            except:
                if tries == 99:
                    print("Error occurred on page ", pag)
                time.sleep(5)
 
        rand_post = list(r.keys())[np.random.randint(0, post_per_page)]        
        timestamp = r[rand_post]['op']['timestamp']
        thread_id = r[rand_post]['op']['thread_num']

        date =  time.ctime(timestamp)
        dict_ids[date[-4:]][date[4:7]].append(thread_id)  #collect thread id and add to list of ids
        
        post, replies = get_4plebs(f'{board}', thread_id)
        del post['thread_num']
        years[int(date[-4:]) - init_year][f"{thread_id}"] = {}
        years[int(date[-4:]) - init_year][f"{thread_id}"]['op'] = post
        years[int(date[-4:]) - init_year][f"{thread_id}"]['replies'] = replies

    
        ## save json every 11 threads added, as a checkpoint in case of errors
        if not pag % 11:
            with open(f"Data/{board}/dict_ids_{gethostname()}.json", 'w', encoding="utf8") as file:
                json.dump(dict_ids, file)
            for year in range(init_year,2022):
                with open(f"Data/{board}/year{year}_{gethostname()}.json", 'w', encoding="utf8") as file:
                    json.dump(years[year-init_year], file)
            
            
    # save final json files
    with open(f"Data/{board}/dict_ids_{gethostname()}.json", 'w', encoding="utf8") as file:
        json.dump(dict_ids, file)
        
    for year in range(init_year, 2022):
        with open(f"Data/{board}/year{year}_{gethostname()}.json", 'w', encoding="utf8") as file:
            json.dump(years[year-init_year], file)

    
if __name__ == "__main__":
    
    board = "pol"  # board abbreviation from which to obtain data
    
    main(board)
