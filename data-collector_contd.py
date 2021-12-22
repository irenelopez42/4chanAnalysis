#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14

@author: Irene Lopez Gutierrez

Collect random posts through time using the 4plebs API. Works for two boards: 'pol' and 'adv'.
"""

import sys
import json
import time
import numpy as np
import archive_utils

# user specific
headers = {'User-Agent': 'abcjoeuigfnm'}   

def main(board):
    
    # create empty dictionary with entries for each month of archive content
    dict_ids = {}
    
    if board == 'pol':
    
        with open("Data/pol/dict_ids.json", 'rb') as file:
            dict_ids = json.load(file)
        
        # open dicts for each year
        years = []
        for year in dict_ids.keys():
            with open(f"Data/pol/year{year}.json", 'rb') as file:
                years.append(json.load(file))
            
        # some info about the 4Plebs archive for /pol/
        resume_from = 1
        init_year = 2013
        until = 821178
        skip_pages = 266
        post_per_page = 10
        
        
    elif board == 'adv':
        
        with open("Data/adv/dict_ids.json", 'rb') as file:
            dict_ids = json.load(file)
        
        # open dicts for each year
        years = []
        for year in dict_ids.keys():
            with open(f"Data/adv/year{year}.json", 'rb') as file:
                years.append(json.load(file))
            
        # some info about the 4Plebs archive for /adv/
        resume_from = 66921
        init_year = 2014
        until = 67205
        skip_pages = 3
        post_per_page = 10
        
    else:
        sys.exit("This board is not supported")

    
    for pag in range(resume_from, until + 1, 1 + skip_pages):
        
        url = f"http://archive.4plebs.org/_/api/chan/index/?board={board}&page={pag}&order=by_thread"

        r = archive_utils.try_request(url, headers)
        r = r.json()
 
        rand_post = list(r.keys())[np.random.randint(0, post_per_page)]        
        timestamp = r[rand_post]['op']['timestamp']
        thread_id = r[rand_post]['op']['thread_num']

        date =  time.ctime(timestamp)
        dict_ids[date[-4:]][date[4:7]].append(thread_id)  #collect thread id and add to list of ids
        
        post, replies = archive_utils.get_4plebs(f'{board}', thread_id)
        del post['thread_num']
        years[int(date[-4:]) - init_year][f"{thread_id}"] = {}
        years[int(date[-4:]) - init_year][f"{thread_id}"]['op'] = post
        years[int(date[-4:]) - init_year][f"{thread_id}"]['replies'] = replies

    
        ## save json every 11 threads added, as a checkpoint in case of errors
        if not pag % 11:
            with open(f"Data/{board}/dict_ids.json", 'w', encoding="utf8") as file:
                json.dump(dict_ids, file)
            for year in range(init_year,2022):
                with open(f"Data/{board}/year{year}.json", 'w', encoding="utf8") as file:
                    json.dump(years[year-init_year], file)
            
            
    # save final json files
    with open(f"Data/{board}/dict_ids.json", 'w', encoding="utf8") as file:
        json.dump(dict_ids, file)
        
    for year in range(init_year, 2022):
        with open(f"Data/{board}/year{year}.json", 'w', encoding="utf8") as file:
            json.dump(years[year-init_year], file)

    
if __name__ == "__main__":
    
    board = "adv"  # board abbreviation from which to obtain data
    
    main(board)