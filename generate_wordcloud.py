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

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] 

df = pd.read_csv("updated-data.csv")
df["date2"] = pd.to_datetime(df["date2"], format="%Y-%m-%d")
df.dropna(axis=0, inplace=True, subset=["paragragh_text", "paragraph_id", "title"])

title = df[["title", "date2"]].drop_duplicates()

year = int(input("Please enter a year:"))
if year not in [2019, 2020, 2021]:
    raise KeyError(f"year {year} does't exist in database!")

fig, axes = plt.subplots(3, 4, figsize=(18, 10))
axes = axes.ravel()

for i in range(12):
    date = datetime(year, i+1, 1)

    month = title[(title["date2"] > date) & (title["date2"] < (date + relativedelta(months=1)))]
    word_counter = Counter()
    month["title"].apply(lambda x: word_counter.update([w.capitalize() for w in TextBlob(x).noun_phrases]))

    del word_counter["Armenia"]
    del word_counter["Pm"]

    img = WordCloud(width=800, height=400).generate_from_frequencies(word_counter)

    axes[i].imshow(img, interpolation='bilinear')
    axes[i].axis("off")
    axes[i].set_title(months[i])

    date = date + relativedelta(months=1)
plt.show()