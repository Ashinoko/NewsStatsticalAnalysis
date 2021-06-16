import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
sns.set_theme(style="whitegrid")


class Graphs:
    def __init__(self):
        self.colors = [(0.9019607843137255, 0.09803921568627451, 0.29411764705882354), (0.23529411764705882, 0.7058823529411765, 0.29411764705882354), (1.0, 0.8823529411764706, 0.09803921568627451), (0.0, 0.5098039215686274, 0.7843137254901961), (0.9607843137254902, 0.5098039215686274, 0.18823529411764706), (0.5686274509803921, 0.11764705882352941, 0.7058823529411765), (0.27450980392156865, 0.9411764705882353, 0.9411764705882353), (0.9411764705882353, 0.19607843137254902, 0.9019607843137255), (0.8235294117647058, 0.9607843137254902, 0.23529411764705882), (0.9803921568627451, 0.7450980392156863, 0.8313725490196079), (0.0, 0.5019607843137255, 0.5019607843137255), (0.8627450980392157, 0.7450980392156863, 1.0), (0.6666666666666666, 0.43137254901960786, 0.1568627450980392), (1.0, 0.9803921568627451, 0.7843137254901961), (0.5019607843137255, 0.0, 0.0), (0.6666666666666666, 1.0, 0.7647058823529411), (0.5019607843137255, 0.5019607843137255, 0.0), (1.0, 0.8431372549019608, 0.7058823529411765), (0.0, 0.0, 0.5019607843137255), (0.5019607843137255, 0.5019607843137255, 0.5019607843137255), (1.0, 1.0, 1.0), (0.0, 0.0, 0.0)]
        df = pd.read_csv("updated-data.csv")
        df["date2"] = pd.to_datetime(df["date2"], format="%Y-%m-%d")
        df.dropna(axis=0, inplace=True, subset=["paragragh_text", "paragraph_id"])
        self.df = df

    def get_set_per_day(self,word):
        word_ind = self.df["paragragh_text"].apply(lambda x: word in x.lower())
        sent_per_day = self.df[word_ind][["date2", "score_by_paragraph"]].groupby("date2").mean()
        sent_per_day = sent_per_day.rolling(45).mean()
        sent_per_day.columns = [word]
        return sent_per_day

    def get_word_freq_day(self,word):
        word_freq = self.df["paragragh_text"].apply(lambda x: x.lower().count(word))
        date2 = self.df[["date2"]].copy()
        date2["freq"] = word_freq
        freq_per_day = date2[["date2", "freq"]].groupby("date2").mean()
        freq_per_day = freq_per_day.rolling(45).mean()
        freq_per_day.columns = [word]
        return freq_per_day

    def get_title_freq_day(self,word):
        title_freq = self.df["title"].apply(lambda x: str(x).lower().count(word))
        date2 = self.df[["date2"]].copy()
        date2["freq"] = title_freq
        title_per_day = date2[["date2", "freq"]].groupby("date2").sum()
        title_per_day = title_per_day.rolling(45).mean()
        title_per_day.columns = [word]
        return title_per_day

    def get_word(self):
        words = ""
        while len(words) == 0:
            words = input("Please enter words seprated by space: ").split()

        return words

    def draw_graphs(self, words):
        fig0, ax0 = plt.subplots(figsize=(16, 8))
        ax0.set_title("Sentiment over time")

        fig1, ax1 = plt.subplots(figsize=(16, 8))
        ax1.set_title("Frequencies of word mentions")
        
        fig2, ax2 = plt.subplots(figsize=(16, 8))
        ax2.set_title("Frequencies of news topics")

        for color, w in zip(self.colors, words):
            sns.lineplot(data=self.get_set_per_day(w), palette=[color], linewidth=2, ax=ax0)

            sns.lineplot(data=self.get_word_freq_day(w), palette=[color], linewidth=2, ax=ax1)

            sns.lineplot(data=self.get_title_freq_day(w), palette=[color], linewidth=2, ax=ax2)

        return fig0, fig1, fig2

    def get_graph_data(self, words):
        g1 = np.stack([self.get_set_per_day(w).values for w in words])
        g2 = np.stack([self.get_word_freq_day(w).values for w in words])
        g3 = np.stack([self.get_title_freq_day(w).values for w in words])
        return g1, g2, g3

    def draw_years_graphs(self):
        words = self.get_word()
        self.draw_graphs(words)


if __name__ == "__main__":
    my_graphs = Graphs()
    my_graphs.draw_years_graphs()