# NewsStatsticalAnalysis
A framework to scrape, analyze and visualize trends and insights from news sources



## Install

You need to install python version +3.8.5

You can download the latest version from [here](https://www.python.org/downloads/)

You need install the requirements
```
pip install -r requirements.txt
```

### Scrapping
Running the code `scraper.py` will start scraping armenpress.com website for news, and stores the results in `data/armenpress/`

### Processing
Running the code `processor.py` will start processing scrapped data from `data/armenpress/`, and creates a `csv` file in the root folder

### Running
The `main.py` will access the `updated-data.csv` to generate graphs and insights.

```
python main.py
```

The `generate_wordclouds.py` will generate wordclouds for each month of a given year.

#### Data

You can access the scraped data [here](https://drive.google.com/file/d/1mYCpbHB1_dCjVp5dEN0Nq3FhwTTrlJxI/view).

You can download the final processed version until (2021/04/23) [here](https://drive.google.com/file/d/1GODohmjsNixT46_6DzMmyXyOiNhrSf1c/view).

## Screenshots

Sentiment: ![alt text](https://github.com/Ashinoko/NewsStatsticalAnalysis/blob/main/screen_shots/Figure_1.png "Sentiment")
Mentions: ![alt text](https://github.com/Ashinoko/NewsStatsticalAnalysis/blob/main/screen_shots/Figure_2.png "Mentions")
Titles: ![alt text](https://github.com/Ashinoko/NewsStatsticalAnalysis/blob/main/screen_shots/Figure_3.png "Titles")
WordCloud: ![alt text](https://github.com/Ashinoko/NewsStatsticalAnalysis/blob/main/screen_shots/Cloud_2020.png "WordCloud")

# Future features
- [ ] More news sources
- [ ] More historical data
- [X] Interactive visualization
- [X] More object oriented structure
- [ ] Better sentiment analysis
- [ ] Other Natural Language Processing models
- [ ] Deploying as a separate website
