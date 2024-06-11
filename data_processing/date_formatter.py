import pandas as pd
from datetime import datetime


class DateFormatter:
    def __init__(self):
        pass

    @staticmethod
    def format_actor_profit(df):
        df["Release Date"] = pd.to_datetime(
            df["Year"].astype(str) + "-" + df["Month"].astype(str),
            format="%Y-%m",
            errors="coerce",
        )
        return df

    @staticmethod
    def format_news(df):
        df["publish_date"] = pd.to_datetime(
            df["publish_date"], format="%Y%m%d", errors="coerce"
        )
        return df

    @staticmethod
    def format_music_popularity(df):
        df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")
        return df

    def format_tv(self, df):
        df["Release Date"] = df["Release Date"].apply(lambda x: self._parse_tv_date(x))
        return df

    @staticmethod
    def _parse_tv_date(date_str):
        if not isinstance(date_str, str):
            return pd.NaT

        # Remove country suffix
        date_str = date_str.split(" (")[0]

        for fmt in ("%d %B %Y", "%B %Y", "%Y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return pd.NaT
