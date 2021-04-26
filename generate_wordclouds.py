from dateutil.relativedelta import relativedelta
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
from textblob import TextBlob
import pandas as pd
import nltk
import re

nltk.download('brown')


class Clouds:
    def __init__(self):
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] 
        self.df = pd.read_csv("updated-data.csv")
        self.df["date2"] = pd.to_datetime(self.df["date2"], format="%Y-%m-%d")
        self.df.dropna(axis=0, inplace=True, subset=["paragragh_text", "paragraph_id", "title"])
        self.title = self.df[["title", "date2"]].drop_duplicates()

    def get_year(self):

        year = int(input("Please enter a year:"))
        if year not in [2019, 2020, 2021]:
            raise KeyError(f"year {year} does't exist in database!")

        return year

    def make_clouds(self,year):

        fig, axes = plt.subplots(3, 4, figsize=(18, 10))
        axes = axes.ravel()

        for i in range(12):
            date = datetime(year, i+1, 1)

            month = self.title[(self.title["date2"] > date) & (self.title["date2"] < (date + relativedelta(months=1)))]
            word_counter = Counter()
            month["title"].apply(lambda x: word_counter.update([w.capitalize() for w in TextBlob(x).noun_phrases]))

            del word_counter["Armenia"]
            del word_counter["Pm"]

            if len(word_counter):
                img = WordCloud(width=800, height=400).generate_from_frequencies(word_counter)

                axes[i].imshow(img, interpolation='bilinear')
                axes[i].axis("off")
                axes[i].set_title(self.months[i])

            date = date + relativedelta(months=1)
        plt.show()

    def make_years_clouds(self):
        year = self.get_year()
        self.make_clouds(year)


if __name__ == "__main__":
    my_cloud = Clouds()
    my_cloud.make_years_clouds()
