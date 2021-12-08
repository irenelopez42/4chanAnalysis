# 4chanAnalysis

This repostory contains the code and data used for a project on a seminar in Computational Social Science at TUM. We implemented tools to obtain data from 4chan archives and analyse the growth of extremist ideologies on the site.

Group members: Benedikt Geitner, Vincent Halasz (@ga42quy), Irene López Gutiérrez (@irenelopez42).

## Data collection

We collect data from two of the most extensive 4chan archives: [4plebs](https://4plebs.org/) and [Archived.moe](https://archived.moe/). We chose 4plebs because of its easily accesible API. However, some of the boards we identified as relevant to our project are not in this archive. Thus, we extended our dataset by performing some web-scrapping on Archived.Moe.

### Data format

Threads collected are stored in json files under `/Data/board/`. There are two types of json files:

- `dict_list.json` files contain a dictionary of thread IDs, stored under the keys for the relevant month and year. For example:

~~~
{"2020": {"Jan": [1,2,3], "Feb": [4,5,6]}, "2021": {"Jan": [7,8,9], "Feb": [10,11,12]}}
~~~

- `year####.json` files contain keys for each thread ID in that year. Each ID has an associated dictionary with two keys: "op" and "replies".
    - Under "op" the following information about the original post is stored: the timestamp (in Unix time), the title, and the comment itself (a.k.a the main text block of the post). 
    - Under "replies" there is a list containing the text of all replies to OP. Only the text is stored for these.


