import ast
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD, Namespace
import os
import urllib.parse


class KnowledgeGraphCreator:
    def __init__(self, prefix):
        self.prefix = prefix
        self.g = Graph()
        self.EX = Namespace("")
        self.load_data()

    def load_data(self):
        self.actor_profit = pd.read_csv(f"{self.prefix}actor_profit.csv")
        self.actor_ratings = pd.read_csv(f"{self.prefix}actor_ratings.csv")
        self.news = pd.read_csv(f"{self.prefix}news.csv")
        self.tv = pd.read_csv(f"{self.prefix}tv.csv")
        self.music_popularity = pd.read_csv(f"{self.prefix}music_popularity.csv")

    def add_actors_to_graph(self):
        for index, row in self.actor_ratings.iterrows():
            if pd.notnull(row).all():
                actor_uri = URIRef(self.EX[str(row["actorName"]).replace(" ", "_")])
                self.g.add((actor_uri, RDF.type, self.EX.Actor))
                self.g.add(
                    (
                        actor_uri,
                        FOAF.name,
                        Literal(row["actorName"], datatype=XSD.string),
                    )
                )
                self.g.add(
                    (
                        actor_uri,
                        self.EX.movieCount,
                        Literal(row["movieCount"], datatype=XSD.integer),
                    )
                )
                self.g.add(
                    (
                        actor_uri,
                        self.EX.ratingSum,
                        Literal(row["ratingSum"], datatype=XSD.float),
                    )
                )
                self.g.add(
                    (
                        actor_uri,
                        self.EX.normalizedMovieRank,
                        Literal(row["normalizedMovieRank"], datatype=XSD.float),
                    )
                )
                self.g.add(
                    (
                        actor_uri,
                        self.EX.googleHits,
                        Literal(row["googleHits"], datatype=XSD.integer),
                    )
                )
                self.g.add(
                    (
                        actor_uri,
                        self.EX.normalizedGoogleRank,
                        Literal(row["normalizedGoogleRank"], datatype=XSD.float),
                    )
                )
                self.g.add(
                    (
                        actor_uri,
                        self.EX.rating,
                        Literal(row["normalizedRating"], datatype=XSD.float),
                    )
                )
        print("Actors added to the graph")

    def add_films_to_graph(self):
        for index, row in self.actor_profit.iterrows():
            if pd.notnull(row).all():
                actor_uri = URIRef(self.EX[row["Actor_name"].replace(" ", "_")])
                film_uri = URIRef(self.EX[row["Film_name"].replace(" ", "_")])
                self.g.add((film_uri, RDF.type, self.EX.Film))
                self.g.add(
                    (
                        film_uri,
                        self.EX.genre,
                        Literal(row["Genre"], datatype=XSD.string),
                    )
                )
                self.g.add(
                    (
                        film_uri,
                        self.EX.gross_profit,
                        Literal(row["Gross_profit"], datatype=XSD.float),
                    )
                )
                self.g.add(
                    (
                        film_uri,
                        self.EX.rating,
                        Literal(row["Ratings"], datatype=XSD.float),
                    )
                )
                self.g.add(
                    (
                        film_uri,
                        self.EX.release_date,
                        Literal(row["Release Date"], datatype=XSD.date),
                    )
                )
                self.g.add((actor_uri, self.EX.acted_in, film_uri))
        print("Films added to the graph")

    def add_tv_shows_to_graph(self):
        for index, row in self.tv.iterrows():
            if pd.notnull(row).all():
                actor_names = row["Stars"].split(", ")
                for actor_name in actor_names:
                    actor_uri = URIRef(self.EX[actor_name.replace(" ", "_")])
                    self.g.add((actor_uri, RDF.type, self.EX.Actor))
                    tv_show_uri = URIRef(self.EX[row["Name"].replace(" ", "_")])
                    self.g.add((tv_show_uri, RDF.type, self.EX.TVShow))
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.duration,
                            Literal(row["Duration"], datatype=XSD.string),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.genre,
                            Literal(row["Genre"], datatype=XSD.string),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.rating,
                            Literal(row["Rating"], datatype=XSD.float),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.no_of_ratings,
                            Literal(row["No. of Ratings"], datatype=XSD.integer),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.no_of_episodes,
                            Literal(row["No. of Episodes"], datatype=XSD.integer),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.creators,
                            Literal(row["Creators"], datatype=XSD.string),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.reviews_users,
                            Literal(row["Reviews (Users)"], datatype=XSD.string),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.reviews_critics,
                            Literal(row["Reviews (Critics)"], datatype=XSD.string),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.seasons,
                            Literal(row["Seasons"], datatype=XSD.integer),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.storyline,
                            Literal(row["Storyline"], datatype=XSD.string),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.language,
                            Literal(row["Language"], datatype=XSD.string),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.release_date,
                            Literal(row["Release Date"], datatype=XSD.date),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.score,
                            Literal(row["score"], datatype=XSD.float),
                        )
                    )
                    self.g.add(
                        (
                            tv_show_uri,
                            self.EX.rating_normalized,
                            Literal(row["score_normalized"], datatype=XSD.float),
                        )
                    )
                    self.g.add((actor_uri, self.EX.acted_in, tv_show_uri))

        print("TV shows added to the graph")

    def add_music_to_graph(self):
        for index, row in self.music_popularity.iterrows():
            if pd.notnull(row).all():
                artist_name = urllib.parse.quote(
                    row["Artists"].replace(" ", "_"), safe="/:"
                )
            artist_uri = URIRef(self.EX[artist_name])
            self.g.add((artist_uri, RDF.type, self.EX.Actor))
            music_name = urllib.parse.quote(row["Name"].replace(" ", "_"), safe="/:")
            music_uri = URIRef(self.EX[music_name])
            self.g.add((music_uri, RDF.type, self.EX.Music))
            self.g.add(
                (
                    music_uri,
                    self.EX.popularity,
                    Literal(row["Popularity"], datatype=XSD.float),
                )
            )
            self.g.add(
                (
                    music_uri,
                    self.EX.artist_name,
                    Literal(row["Artists"], datatype=XSD.string),
                )
            )
            self.g.add(
                (
                    music_uri,
                    self.EX.normalized_name,
                    Literal(row["Normalized Name"], datatype=XSD.string),
                )
            )
            self.g.add(
                (
                    music_uri,
                    self.EX.release_date,
                    Literal(row["Release Date"], datatype=XSD.date),
                )
            )
            self.g.add(
                (
                    music_uri,
                    self.EX.rating_normalized,
                    Literal(row["Normalized Popularity"], datatype=XSD.float),
                )
            )
            self.g.add((artist_uri, self.EX.performed, music_uri))

        print("Music added to the graph")

    def add_news_to_graph(self):
        for index, row in self.news.iterrows():
            if pd.notnull(row).all():
                headline_text = urllib.parse.quote(
                    str(row["headline_text"]).replace(" ", "_"), safe="/:"
                )
                news_uri = URIRef(self.EX[headline_text])
                self.g.add((news_uri, RDF.type, self.EX.News))
                self.g.add(
                    (
                        news_uri,
                        self.EX.publish_date,
                        Literal(row["publish_date"], datatype=XSD.date),
                    )
                )
                self.g.add(
                    (
                        news_uri,
                        self.EX.headline_category,
                        Literal(row["headline_category"], datatype=XSD.string),
                    )
                )
                self.g.add(
                    (
                        news_uri,
                        self.EX.headline_text,
                        Literal(row["headline_text"], datatype=XSD.string),
                    )
                )
                # Parse the Subjects string
                subjects = ast.literal_eval(row["Subjects"])
                for subject in subjects:
                    subject_uri = URIRef(self.EX[subject.replace(" ", "_")])
                    self.g.add((news_uri, self.EX.subject, subject_uri))
                    self.g.add((subject_uri, self.EX.mentioned, news_uri))

                self.g.add(
                    (
                        news_uri,
                        self.EX.mentions,
                        Literal(row["Mentions"], datatype=XSD.integer),
                    )
                )
                self.g.add(
                    (
                        news_uri,
                        self.EX.ratings,
                        Literal(row["Ratings"], datatype=XSD.float),
                    )
                )
        print("News articles added to the graph")

    def create_graph(self):
        self.add_actors_to_graph()
        self.add_films_to_graph()
        self.add_tv_shows_to_graph()
        self.add_music_to_graph()
        self.add_news_to_graph()
        print("Graph created successfully!")

    def save_graph(self, file_name="knowledge_graph.ttl"):
        self.g.serialize(file_name, format="turtle")
        print(f"Graph saved to {file_name}")

    def query_graph(self, query, var1, var2, var3):
        for row in self.g.query(query):
            print(
                f"{var1}: {getattr(row, var1)}, {var2}: {getattr(row, var2)}, {var3}: {getattr(row, var3)}"
            )


if __name__ == "__main__":
    prefix = os.getcwd() + "/datasets/"
    kg_creator = KnowledgeGraphCreator(prefix)
    kg_creator.create_graph()
    kg_creator.save_graph()
