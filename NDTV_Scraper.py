"""
Will require the installations of folowing modules
- bs4 (beautifulSoup)
- requests
- json
- lxml
"""

import json
import bs4
from bs4 import BeautifulSoup 
import requests

#List of dictionaries to save all each news dict object
list_of_dict = []

def ndtv_main(main_url):
    base_res = requests.get(main_url)
    base_soup = BeautifulSoup(base_res.text, 'lxml')
    pagination = base_soup.find('div', {'class': 'new_pagination'}).findAll('a')

    for page in pagination:
        next_url = page['href']
        res = requests.get(next_url)
        soup = BeautifulSoup(res.text, 'lxml')
        div = soup.find('div', {'class': 'new_storylising'}).findAll('li')
        for x in div:
            des = x.find('div', {'class': 'nstory_intro'})
            pub = x.find('div', {'class': 'nstory_dateline'})
            t = x.find('a')
            img = x.find('img')
            preProcess(pub, des, t, img)
    final_json_file = json.dumps(list_of_dict, indent = 4)
    return final_json_file


#Checking for NULL property values & apending to the dictionary
def preProcess(pub, des, t, img):
    d = {}
    d['source'] = 'NDTV.com'
    
    if(t is not None):
        d['title'] = t['title']
        d['url'] = t['href']
    else:
        d['title'] = None
        d['url'] = None
    if(des is not None):
        d['description'] = des.text
    else:
        d['description'] = None

    if(img is not None):
        d['urlToImage'] = img['src']
    else:
        d['urlToImage'] = None
    
    if(pub is not None):
        auth = pub.text.split('|')
        d['author'] = auth[0].strip()
        d['publishedAt'] = auth[1].strip()
    else:
        d['author'] = None
        d['publishedAt'] = None
    
    #Appending the dict to list of dictionaries
    list_of_dict.append(d)
