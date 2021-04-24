import bs4
import requests
import datetime
import json
from glob import glob
import os
import re
from time import time



DOMAIN = "https://armenpress.am"
headers = {'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}
url_of_allthemes = 'https://armenpress.am/eng/news/allthemes/'

today = datetime.date.today()
today = str(today.strftime('%Y/%m/%d'))

json_files = glob("data/armenpress/*.json")

if len(json_files):
    date = []
    for json_path in json_files:
        date.append(os.path.basename(json_path).replace('.json',''))

    date = [datetime.datetime.strptime(d, "%Y_%m_%d") for d in date]
    latest_saved_date = max(date).strftime("%Y/%m/%d")
    date1 = latest_saved_date
else:
    date1 = "2018/01/01"

date2 = today
start = datetime.datetime.strptime(date1, '%Y/%m/%d')
end = datetime.datetime.strptime(date2, '%Y/%m/%d')
step = datetime.timedelta(days=1)


print('\n\n'+'current day :'+ today+'\n\n')
print('\n\n'+'latest date :'+ date1+'\n\n')


while start <= end:
    start_time = time()
    #print(start.strftime('%Y/%m/%d'))

    link_of_the_day = url_of_allthemes + start.strftime('%Y/%m/%d')+'/'
    #res = requests.get("https://armenpress.am/eng/news/allthemes/2020/09/01/", headers=headers)
    res = requests.get(link_of_the_day, headers=headers)

    soup = bs4.BeautifulSoup(res.content)
    elements = soup.findAll("article", {"class": "newsbycatitem"})
    news_of_the_day = []

    for elem in elements:
        title_n_time = elem.text
        #print(title_n_time)
        try:
            title, _time = title_n_time.strip().split("\n\n\n")
        except ValueError:
            print('TITLE ERROR')
            title, _time = "DELETED", title_n_time.strip()

        url = DOMAIN + elem.findAll("a")[0]["href"]
        page_res = requests.get(url, headers=headers)
        page_html = page_res.content
        page_soup = bs4.BeautifulSoup(page_html, features="lxml")
        try:
            paragraphs = page_soup.findAll("span", {"itemprop": "articleBody"})[0].text.strip().split("\n")
        except IndexError:
            print('PARAGRAPH ERROR')
            paragraphs = []
        news_of_the_day.append({'title': title, 'url': url, 'content_by_paragraph': paragraphs, 'date': _time})
        #print(title, time, url, sep="|")
        #print(len(paragraphs), paragraphs[0], sep="|", end="\n\n" + "==" * 20 + "\n\n")
    #print(news_of_the_day)
    #with open('armenpress/2020_09_01.json', "w+") as json_file:
    #    json.dump(news_of_the_day,json_file)
    with open('data/armenpress/' +start.strftime('%Y_%m_%d') + '.json', "w+") as json_file:
        json.dump(news_of_the_day, json_file)
    print(time()-start_time, start.strftime('%Y/%m/%d'))
    start += step
