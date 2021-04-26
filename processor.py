import pandas as pd
import json
import os
from textblob import TextBlob
from transformers import pipeline
from glob import glob
from tqdm import tqdm


class Processor:
    def __init__(self, data_path="data/armenpress/"):
        self.json_files = glob(f"{data_path}*.json") 

    def process_data(self, destination_folder="data/armenpress/"):

        os.makedirs(destination_folder, exist_ok=True)

        classifier = pipeline('sentiment-analysis')

        for json_path in tqdm(self.json_files):
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

            self.store_json(destination_folder, data_day, date)

    def store_json(self, destination_folder, data, name):
        if len(data) !=0:
            fname = os.path.join(destination_folder, name+".json")
            with open(fname, "w+") as f:
                json.dump(data, f)

    def store_csv(self):
        all_data = []
        for json_path in tqdm(self.json_files):
            with open (json_path) as f:
                day = json.load(f)
            all_data.extend(day)

        df = pd.DataFrame(all_data)
        df["date2"] = pd.to_datetime(df["date2"], format="%Y_%m_%d")
        df.to_csv("updated-data.csv", index=False)


    def process_store_csv(self):
        self.process_data()
        self.store_csv()

if __name__ == "__main__":
    y_processor = Processor()
    my_processor.process_data()
