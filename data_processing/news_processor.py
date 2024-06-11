import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from textblob import TextBlob as tb


class NewsProcessor:
    def __init__(self, subjects=None):
        self.subjects = subjects

    def process_headlines(self, news_df, headlines):
        lowered_subjects = [subject.lower() for subject in self.subjects]
        lowered_headlines = [headline.lower() for headline in headlines]
        subjects_column = []
        subject_counts_column = []

        for headline in lowered_headlines:
            subjects_in_headline = []
            headline_subject_count = 0
            for subject in lowered_subjects:
                # Check if the subject is in the headline
                if subject in headline:
                    subjects_in_headline.append(subject)
                    headline_subject_count += 1
            subjects_column.append(subjects_in_headline)
            subject_counts_column.append(headline_subject_count)

        news_df["Subjects"] = subjects_column
        news_df["Mentions"] = subject_counts_column

        return self.extract_semantics(news_df, headlines)

    def normalize_mentions(self, news_df):
        news_df["Ratings"] = np.log1p(news_df["Mentions"])
        scaler = MinMaxScaler(feature_range=(1, 10))
        news_df["Ratings"] = scaler.fit_transform(news_df[["Mentions"]])
        return news_df

    def extract_semantics(self, news_df, headlines):
        news_df["Sentiment"] = [
            (
                "positive"
                if tb(headline).sentiment.polarity > 0
                else ("negative" if tb(headline).sentiment.polarity < 0 else "neutral")
            )
            for headline in headlines
        ]

        return news_df

    def get_news(self, news_df):
        return news_df
