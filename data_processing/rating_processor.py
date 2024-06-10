import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class RatingsProcessor:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(1, 10))

    @staticmethod
    def process_actor_ratings(actor_rating_df):
        return actor_rating_df

    @staticmethod
    def process_actor_profit(actor_profit_df):
        scaler = MinMaxScaler(feature_range=(1, 10))
        actor_profit_df["Ratings"] = scaler.fit_transform(
            actor_profit_df[["Gross_profit"]]
        )
        return actor_profit_df

    @staticmethod
    def process_tv_shows(tv_df):
        C = tv_df["Rating"].mean()
        m = tv_df["No. of Ratings"].quantile(0.05)
        tv_shows = tv_df.copy().loc[tv_df["No. of Ratings"] >= m]
        tv_shows["score"] = tv_shows.apply(
            lambda x: RatingsProcessor.weighted_rating(x, m, C), axis=1
        )
        tv_shows["score_normalized"] = (tv_shows["score"] - 1) / (10 - 1)
        tv_shows = tv_shows.sort_values("score_normalized", ascending=False)
        return tv_shows

    @staticmethod
    def weighted_rating(x, m, C):
        v = x["No. of Ratings"]
        R = x["Rating"]
        return (v / (v + m) * R) + (m / (m + v) * C)

    @staticmethod
    def process_music_popularity(music_df):
        scaler = MinMaxScaler(feature_range=(1, 10))
        music_df["Normalized Popularity"] = scaler.fit_transform(
            music_df[["Popularity"]]
        )
        return music_df
