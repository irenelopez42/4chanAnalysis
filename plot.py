"""
Created on Fri Dec 10 20:53:47 2021

@author: Irene López

Count all threads + replies and plot them by date
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import pickle
from archive_utils import mon_to_number

boards = ["sci", "news", "pol", "adv"]
n_threads = []  #empty list to store number of posts per month
n_posts = [] # list to store number of comments per month
dates = []

for board in boards:
    
    n_threads_board = []
    n_posts_board = []
    dates_board = []

    # open dict with all thread IDs
    with open(f"Data/{board}/dict_ids.json", 'r') as file:
        dict_ids = json.load(file)
        
    # for each year and month, count number of thread and posts
    for year in dict_ids.keys():
        
        year_dict = dict_ids[year]
        
        for month in year_dict.keys():
            
            mon = mon_to_number(month)
            td_year = year[-2:]
            dates_board.append(f"{mon}/{td_year}")
            
            # count number of threads in this month
            month_ids = year_dict[month]
            n_threads_month = len(month_ids)
            n_threads_board.append(n_threads_month)
            
            #open dict with threads data
            with open(f"Data/{board}/year{year}.json", 'r') as file:
                dict_posts = json.load(file)
              
            # count number of replies in all threads for this month
            n_replies = 0
            for thread in month_ids:
                replies = dict_posts[f"{thread}"]["replies"]
                n_replies += len(replies)
                
            n_posts_board.append(n_replies)
            
    n_threads.append(n_threads_board)
    n_posts.append(n_posts_board)
    dates.append(dates_board)
    
    
with open("Plots/n_threads.pickle", 'wb') as file:
    pickle.dump(n_threads, file)
with open("Plots/n_posts.pickle", 'wb') as file:
    pickle.dump(n_posts, file)
with open("Plots/dates.pickle", 'wb') as file:
    pickle.dump(dates, file)
    
pol_max = np.argmax(n_threads[2])
news_max = np.argmax(n_threads[1])
    
plt.plot(dates[0], n_threads[0], label=boards[0])
plt.plot(dates[1], n_threads[1], label=boards[1])
plt.plot(dates[2], n_threads[2], label=boards[2])
plt.plot(dates[3], n_threads[3], label=boards[3])
plt.legend()
plt.xticks([dates[0][0], dates[2][0], dates[1][0], dates[1][news_max],
            dates[2][pol_max], dates[0][-1]], rotation=50)
plt.ylabel("Number of threads")
plt.xlabel("Date")
plt.savefig("Plots/n_threads.pdf")
plt.show()

plt.plot(dates[0], np.array(n_threads[0]) + np.array(n_posts[0]), label=boards[0])
plt.plot(dates[1], np.array(n_threads[1]) + np.array(n_posts[1]), label=boards[1])
plt.plot(dates[2], np.array(n_threads[2]) + np.array(n_posts[2]), label=boards[2])
plt.plot(dates[3], np.array(n_threads[3]) + np.array(n_posts[3]), label=boards[3])
plt.legend()
plt.xticks([dates[0][0], dates[2][0], dates[1][0], dates[1][news_max],
            dates[2][pol_max], dates[0][-1]], rotation=50)
plt.ylabel("Number of posts")
plt.xlabel("Date")
plt.savefig("Plots/n_posts.pdf")


total_threads_per_board = [sum(i) for i in n_threads]
total_replies_per_board = [sum(i) for i in n_posts]
print("Total number of threads:", sum(total_threads_per_board))
print("Total number of posts:", sum(total_threads_per_board) + sum(total_replies_per_board))

print("Total number of threads per board: \n", total_threads_per_board)
print("Total number of posts per board: \n", np.array(total_threads_per_board)
                                          + np.array(total_replies_per_board))
