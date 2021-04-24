import pandas as pd
import json
import os
from textblob import TextBlob
from transformers import pipeline
from glob import glob
from tqdm import tqdm

json_files = glob("data/armenpress/*.json")
destination_folder = "data/armenpress/"
os.makedirs(destination_folder, exist_ok=True)

classifier = pipeline('sentiment-analysis')

for json_path in tqdm(json_files):
    data_day = []
    date = os.path.basename(json_path).replace('.json','')
    with open (json_path) as f:
        day = json.load(f)
    for news in day:
        if "date2" not in news:
            news['source'] = 'https://armenpress.am'
            news['date2'] = date
            for i, para in enumerate(news["content_by_paragraph"]):
                paragraph = news.copy()
                paragraph["paragragh_text"] = para
                paragraph["paragraph_id"] = i
                result = classifier(para[:512])[0]
                if result["label"] == "POSITIVE":
                    score = result["score"]
                elif result["label"] == "NEGATIVE":
                    score = 1 - result["score"]
                else:
                    raise AttributeError(f"classifier returned something not pos/neg {result['label']}")
                paragraph["score_by_paragraph"] = score
                data_day.append(paragraph)
    if len(data_day) !=0:
        fname = os.path.join(destination_folder, date+".json")
        with open(fname, "w+") as f:
            json.dump(data_day, f)

all_data = []
for json_path in tqdm(json_files):
    with open (json_path) as f:
        day = json.load(f)
    all_data.extend(day)

df = pd.DataFrame(all_data)
df["date2"] = pd.to_datetime(df["date2"], format="%Y_%m_%d")
df.to_csv("updated-data.csv", index=False)
