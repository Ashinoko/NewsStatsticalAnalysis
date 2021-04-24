# NewsStatsticalAnalysis
A framework to scrape, analyze and visualize trends and insights from news sources

This project initialized as course project for university.

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
Running the code `processor.py` will start processing scrapped data from `data/armenpress/, and creates a `csv` file in the root folder

### Running
The `main.py` will access the `updated-data.csv` to generate graphs and insights.

```
python main.py
```

The `generate_wordcloud.py` will generate wordclouds for each month of a given year.

