"""
Created on Mon Dec  6 18:34:57 2021

@author: Irene Lopez Gutierrez

File to do some web-scrapping on archived.moe to obtain data for boards /sci/ and /news/
"""

import sys
import requests
import re
from bs4 import BeautifulSoup
import datetime
import time
import json


# user specific
headers = {'User-Agent': 'adbsfkjrgn'}

def main(board):
    
    # empty dict to collect ids for each year & month
    dict_ids = {}
    
    
    if board == 'sci':
        # year and month keys for /sci/
        dict_ids["2010"] = {"May": [], "Jun": [], "Jul": [], "Aug": [], "Sep": [], 
                        "Oct": [], "Nov": [], "Dec": []}
        
        for year in range(2011, 2022):
                dict_ids[ f"{year}" ] = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], 
                        "May": [], "Jun": [], "Jul": [], "Aug": [], "Sep": [], 
                        "Oct": [], "Nov": [], "Dec": []} 
                
        # create empty dict for each year
        years = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
            
        # some info about the archived.moe archive for /sci/
        init_year = 2010
        total_pages = 62581
        skip_pages = 20
        
        
    elif board == 'news':
        # year and month keys for sci
        dict_ids["2015"] = {"Nov": [], "Dec": []}
        for year in range(2016, 2022):
            dict_ids[ f"{year}" ] = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], 
                    "May": [], "Jun": [], "Jul": [], "Aug": [], "Sep": [], 
                    "Oct": [], "Nov": [], "Dec": []}
            
        # create empty dict for each year
        years = [{}, {}, {}, {}, {}, {}, {}]
            
        # some info about the 4Plebs archive for /adv/
        init_year = 2015
        total_pages = 3157
        skip_pages = 0
        
    else:
        sys.exit("This board is not supported")
    
    
    for pag in range(1, total_pages, 1 + skip_pages):
        
        # request access to page and get one thread id
        url = f"https://archived.moe/{board}/page/{pag}"
        # tries to acces url. If access denied, sleep 5 seconds. Maximum tries = 100
        for tries in range(100):
            try:
                r = requests.get(url, headers=headers)
                r.raise_for_status()
                break
                    
            except:
                if tries == 99:
                    print("Error occurred on page ", pag)
                    sys.exit("Request access denied 100 times.")
                time.sleep(5)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        posts = soup.find_all("div", {"class": re.compile("thread stub")})
        id_post = posts[0].button['data-thread-num']  # id from first post in page
        
        
        # request access to thread and get important info
        url = f"https://archived.moe/{board}/thread/{id_post}"
        # tries to acces url. If access denied, sleep 5 seconds. Maximum tries = 100
        for tries in range(100):
            try:
                r = requests.get(url, headers=headers)
                r.raise_for_status()
                break
                    
            except:
                if tries == 99:
                    print("Error occurred on page ", pag)
                    sys.exit("Request access denied 100 times.")
                time.sleep(5)
                
        post = BeautifulSoup(r.text, 'html.parser')
        
        title = post.find('h2', {'class': "post_title"}).text
        
        date = post.find('time').text
        day, month, year = date[4:6], date[7:10], date[11:15]
        date = day + f"/{mon_to_number(month)}/" + year
        timestamp = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())
    
        comment = post.find('div', {'class': 'text'}).text
        
        op = {'timestamp': int(timestamp), 'title': title, 'comment': comment}
        
        replies = post.find('aside', {'class': 'posts'})
        replies = replies.find_all("article")
        n_replies = len(replies)
        replies_text = []  # empty list to collect all text in replies
        for rep in range(n_replies):
            replies_text.append( replies[rep].find('div', {'class': 'text'}).text )
        
        
        # store all collected date into dictionaries
        dict_ids[year][month].append(id_post)
        years[int(year) - init_year][f'{id_post}'] = {}
        years[int(year) - init_year][f'{id_post}']['op'] = op
        years[int(year) - init_year][f'{id_post}']['replies'] = replies_text
        
        ## save json every 3 threads added, as a checkpoint in case of errors
        if not pag % 3:
            with open(f"Data/{board}/dict_ids.json", 'w', encoding="utf8") as file:
                json.dump(dict_ids, file)
            for year in range(init_year,2022):
                with open(f"Data/{board}/year{year}.json", 'w', encoding="utf8") as file:
                    json.dump(years[year-init_year], file)
                    
    # save final json files
    with open(f"Data/{board}/dict_ids.json", 'w', encoding="utf8") as file:
        json.dump(dict_ids, file)
        
    for year in range(init_year,2022):
        with open(f"Data/{board}/year{year}.json", 'w', encoding="utf8") as file:
            json.dump(years[year-init_year], file)
    

    
if __name__ == '__main__':
    
    board = 'news'
    main(board)