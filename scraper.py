import bs4
import requests
import datetime
import json
from glob import glob
import os
import re
from time import time


class Scraper:
    def __init__(self, data_path="data/armenpress/"):
        self.DOMAIN = "https://armenpress.am"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}
        self.url_of_allthemes = 'https://armenpress.am/eng/news/allthemes/'
        self.json_files = glob(f"{data_path}*.json")
        self.data_path = "data/armenpress/"

    def get_todays_date(self):
        return datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

    def get_latest_date(self):
        if len(self.json_files):
            date = []
            for json_path in self.json_files:
                date.append(os.path.basename(json_path).replace('.json',''))

            date = [datetime.datetime.strptime(d, "%Y_%m_%d") for d in date]
            latest_saved_date = max(date).strftime("%Y/%m/%d")
            date1 = latest_saved_date
        else:
            date1 = "2018/01/01"

        start = datetime.datetime.strptime(date1, '%Y/%m/%d')

        return start

    def store_json(self, data, name):
        with open(self.data_path + name.strftime('%Y_%m_%d') + '.json', "w+") as json_file:
            json.dump(data, json_file)

    def scrape(self, start, end):
        step = datetime.timedelta(days=1)

        print("Scraping from "+ str(start)+" to " + str(end))

        while start <= end:
            start_time = time()

            link_of_the_day = self.url_of_allthemes + start.strftime('%Y/%m/%d')+'/'

            res = requests.get(link_of_the_day, headers=self.headers)

            soup = bs4.BeautifulSoup(res.content, features="lxml")
            elements = soup.findAll("article", {"class": "newsbycatitem"})
            news_of_the_day = []

            for elem in elements:
                title_n_time = elem.text
                try:
                    title, _time = title_n_time.strip().split("\n\n\n")
                except ValueError:
                    print('TITLE ERROR')
                    title, _time = "DELETED", title_n_time.strip()

                url = self.DOMAIN + elem.findAll("a")[0]["href"]
                page_res = requests.get(url, headers=self.headers)
                page_html = page_res.content
                page_soup = bs4.BeautifulSoup(page_html, features="lxml")
                try:
                    paragraphs = page_soup.findAll("span", {"itemprop": "articleBody"})[0].text.strip().split("\n")
                except IndexError:
                    print('PARAGRAPH ERROR')
                    paragraphs = []
                news_of_the_day.append({'title': title, 'url': url, 'content_by_paragraph': paragraphs, 'date': _time})
            self.store_json(news_of_the_day, start)
            print(time()-start_time, start.strftime('%Y/%m/%d'))
            start += step

    def update_data(self):
        date1 = self.get_latest_date()
        date2 = self.get_todays_date()
        self.scrape(date1,date2)


if __name__ == "__main__":
    my_scraper = Scraper()
    my_scraper.update_data()
