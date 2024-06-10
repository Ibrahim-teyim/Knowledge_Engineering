import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import MinMaxScaler


class NewsProcessor:
    def __init__(self, subjects=None):
        self.subjects = subjects

    def process_headlines(self, headlines):
        lowered_subjects = [subject.lower() for subject in self.subjects]
        lowered_headlines = [headline.lower() for headline in headlines]
        subject_counts = Counter()
        for headline in lowered_headlines:
            for subject in lowered_subjects:
                if subject in headline:
                    subject_counts[subject] += 1
        return subject_counts

    def normalize_mentions(self, subject_counts):
        subject_counts_df = pd.DataFrame(
            subject_counts.items(), columns=["Subject", "Mentions"]
        )
        subject_counts_df = subject_counts_df[subject_counts_df["Subject"] != "dev"]
        subject_counts_df["Mentions"] = np.log1p(subject_counts_df["Mentions"])
        scaler = MinMaxScaler(feature_range=(1, 10))
        subject_counts_df["Ratings"] = scaler.fit_transform(
            subject_counts_df[["Mentions"]]
        )
        return subject_counts_df

    def get_news(self, news_df):
        return news_df
