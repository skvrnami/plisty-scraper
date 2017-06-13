#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parlamentnilisty.cz Scrapper

@author: skvrnami
"""

## import libraries
from bs4 import BeautifulSoup
import requests, sys
import pandas as pd

## scrap for number of pages within the news section
page = 1
params = {"p": page}
r = requests.get("http://www.parlamentnilisty.cz/zpravy", params=params)
soup = BeautifulSoup(r.text, "html.parser")

## find out how many pages there are in total
pagination = soup.find("div", {"class": "pagination"})
p = pagination.findAll("a")
pages_list = []
for page in p:
    pages_list.append(page.text)

## number of pages in the section (the fifth element in the div pagination)
end_page = int(pages_list[4])

## scrap from the first page to the last
article_names = []
article_links = []
article_dates = []

for page in range(1, end_page + 1):
    print("Processing page: ", str(page))
    params = {"p": page}
    r = requests.get("http://www.parlamentnilisty.cz/zpravy", params=params)
    soup = BeautifulSoup(r.text, "html.parser")
    articles_col = soup.find("div", {"class": "col-md-8"})
    
    ## find all titles of articles in the article section
    a_names = articles_col.findAll("h2")
    
    ## get rid of the HTML tag
    for i in range(0, len(a_names)):
        a_names[i] = a_names[i].get_text()
    
    ## find all links in the article section
    a_links = articles_col.findAll("a")

    ## extract url links only
    links = []
    for link in a_links:
        ## create functional URL by adding PL.cz to relative link
        ## and get rid of URLs to other pages
        if not link.get("href") == "/zpravy":
            if not "/zpravy?p" in link.get("href"):
                links.append("http://www.parlamentnilisty.cz" + link.get("href"))
   
    ## find date of publication and create list (dates_list)
    articles_time = articles_col.findAll("span", {"class":"time"})
    a_dates = []
    for date in articles_time:
        a_dates.append(date.text)
    
    if len(a_names) != len(links):
        sys.exit('The number of articles and links differ')    
    
    article_names += a_names
    article_links += links
    article_dates += a_dates
    
    
## create dataframe
index = list(range(1, len(article_names) + 1))
columns = ['name', 'url', 'date']
df = pd.DataFrame(index=index, columns=columns)
df.name = article_names
df.url = article_links
df.date = article_dates

## save the dataframe to .csv file
df.to_csv("plisty.csv", sep=',', encoding='utf-8')