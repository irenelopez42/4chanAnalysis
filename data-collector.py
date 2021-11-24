#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:37:32 2021

@author: Irene Lopez Gutierrez

Collect random /pol/ posts through time using the 4plebs API 
"""

import requests
import json
import time
import numpy as np
from subprocess import call
from socket import gethostname
from archive import get_4plebs

# user specific
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}   

# some info about 4Plebs
total_pages = 821178
post_per_page = 10

def main():
    
    # create empty dictionary with entries for each month of archive content
    dict_ids = {}
    
    dict_ids["2013"] = {"Nov": [], "Dec": []}
    
    for year in range(2014, 2021):
        dict_ids[ f"{year}" ] = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], 
                "May": [], "Jun": [], "Jul": [], "Aug": [], "Sep": [], 
                "Oct": [], "Nov": [], "Dec": []}
        
    dict_ids["2021"] = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], 
                "May": [], "Jun": [], "Jul": [], "Aug": [], "Sep": [], 
                "Oct": [], "Nov": []}
    
    
    # create empty dict for each year
    years = [{}, {}, {}, {}, {}, {}, {}, {}, {}]
    
    for pag in range(1, total_pages + 1, 80):
        
        url = f"http://archive.4plebs.org/_/api/chan/index/?board=pol&page={pag}&order=by_thread"

        # tries to acces url. If access denied, sleep 5 seconds. Maximum tries = 100
        for tries in range(100):
            try:
                r = requests.get(url, headers=headers)
                r.raise_for_status()
                r = r.json()
                break
                    
            except:
                time.sleep(5)
 
        rand_post = list(r.keys())[np.random.randint(0,10)]        
        timestamp = r[rand_post]['op']['timestamp']
        thread_id = r[rand_post]['op']['thread_num']

        date =  time.ctime(timestamp)
        dict_ids[date[-4:]][date[4:7]].append(thread_id)  #collect thread id and add to list of ids
        
        post, replies = get_4plebs('pol', thread_id)
        del post['thread_num']
        years[int(date[-4:]) - 2013][f"{thread_id}"] = {}
        years[int(date[-4:]) - 2013][f"{thread_id}"]['op'] = post
        years[int(date[-4:]) - 2013][f"{thread_id}"]['replies'] = replies

    
        ## save json every 11 threads added, as a checkpoint in case of errors
        if not pag % 11:
            with open(f"dict_ids_{gethostname()}.json", 'w', encoding="utf8") as file:
                json.dump(dict_ids, file)
            for year in range(2013,2022):
                with open(f"year{year}_{gethostname()}.json", 'w', encoding="utf8") as file:
                    json.dump(years[year-2013], file)
            
            
    with open(f"dict_ids_{gethostname()}.json", 'w', encoding="utf8") as file:
        json.dump(dict_ids, file)
        
    for year in range(2013,2022):
        with open(f"year{year}_{gethostname()}.json", 'w', encoding="utf8") as file:
            print("\n TEST \n", years[year-2013])
            json.dump(years[year-2013], file)
    
    call("./push.sh")

    
if __name__ == "__main__":
    main()
