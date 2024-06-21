from data_processing.data_loader import DataLoader
from data_processing.date_formatter import DateFormatter
from data_processing.music_release_date_fetcher import ReleaseDateFetcher
from data_processing.news_processor import NewsProcessor
from data_processing.rating_processor import RatingsProcessor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


TO_EDIT_PREFIX = "to_edit_data/"
DATASET_PREFIX = "datasets/"


def create_data():
    loader = DataLoader(TO_EDIT_PREFIX, DATASET_PREFIX)

    # Process news
    news_df = loader.load_csv("news.csv")
    tv_df = loader.load_csv("tv.csv")
    actor_profit_df = loader.load_csv("actor_profit.csv")
    actor_rating_df = loader.load_csv("actor_ratings.csv")
    music_df = loader.load_csv("spotify.csv")

    # Process actor ratings
    actor_rating_df = process_actor_ratings(actor_rating_df)

    # Process actor profit
    actor_profit_df = process_actor_profit(loader, actor_profit_df)

    # Process TV shows ratings
    tv_df = process_tv_shows(loader, tv_df)

    # Get release dates and process music popularity
    music_df = process_music_popularity(loader, process_release_dates(music_df))

    subjects = extract_subjects(tv_df, actor_profit_df, actor_rating_df, music_df)
    news_df = process_news(remove_duplicates(news_df), subjects)

    format_dates(
        actor_profit_df=actor_profit_df, news_df=news_df, music_df=music_df, tv_df=tv_df
    )


def process_release_dates(df):
    fetcher = ReleaseDateFetcher(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    df["Normalized Name"] = (
        df["Name"].str.replace(r"\(.*\)", "", regex=True).str.strip()
    )
    df["Release Date"] = None
    df = fetcher.fetch_release_dates_concurrently(df)
    return df


def extract_subjects(tv_df, actor_profit_df, actor_rating_df, music_df):
    return list(
        set(
            tv_df["Stars"]
            .str.replace("[", "")
            .str.replace("]", "")
            .str.replace("'", "")
            .str.split(", ")
            .explode()
            .dropna()
            .apply(lambda x: x.strip())
            .loc[lambda x: x != ""]
            .tolist()
            + actor_profit_df["Actor_name"].tolist()
            + actor_rating_df["actorName"].tolist()
            + music_df["Artists"].str.split(", ").explode().tolist()
        )
    )


def process_news(news_df, subjects):
    news_processor = NewsProcessor(subjects)
    news_df = news_processor.process_headlines(news_df=news_df)
    news_df = news_processor.normalize_mentions(news_df)
    return news_df


def process_actor_ratings(actor_rating_df):
    actor_ratings_df = RatingsProcessor.process_actor_ratings(actor_rating_df)
    return actor_ratings_df


def process_actor_profit(loader, actor_profit_df):
    actor_profit_df = RatingsProcessor.process_actor_profit(actor_profit_df)
    return actor_profit_df


def process_tv_shows(loader, tv_df):
    tv_shows_df = RatingsProcessor.process_tv_shows(tv_df)
    return tv_shows_df


def process_music_popularity(loader, music_df):
    music_popularity_df = RatingsProcessor.process_music_popularity(music_df)
    return music_popularity_df


def remove_duplicates(df):
    df = df.drop_duplicates(subset=["headline_text"])
    return df


def format_dates(actor_profit_df, news_df, music_df, tv_df):
    # Load updated files
    loader = DataLoader(DATASET_PREFIX, DATASET_PREFIX)

    formatter = DateFormatter()
    actor_profit_df = formatter.format_actor_profit(actor_profit_df)
    news_df = formatter.format_news(news_df)
    music_df = formatter.format_music_popularity(music_df)
    tv_df = formatter.format_tv(tv_df)
    loader.save_csv(actor_profit_df, "actor_profit.csv")
    loader.save_csv(news_df, "news.csv")
    loader.save_csv(music_df, "music_popularity.csv")
    loader.save_csv(tv_df, "tv.csv")


if __name__ == "__main__":
    create_data()
