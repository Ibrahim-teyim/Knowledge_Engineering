import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class ReleaseDateFetcher:
    def __init__(self, spotify_client_id, spotify_client_secret):
        self.spotify = self.setup_spotify(spotify_client_id, spotify_client_secret)

    def setup_spotify(self, client_id, client_secret):
        spotify_client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        return spotipy.Spotify(
            client_credentials_manager=spotify_client_credentials_manager
        )

    def get_release_date_musicbrainz(self, song_name, artist):
        base_url = "https://musicbrainz.org/ws/2/recording/"
        headers = {"User-Agent": "MusicDataFetcher/1.0 (your-email@example.com)"}
        params = {
            "query": f'recording:"{song_name}" AND artist:"{artist}"',
            "fmt": "json",
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if "recordings" in data and len(data["recordings"]) > 0:
                return data["recordings"][0].get("first-release-date", None)
        return None

    def get_release_date_spotify(self, song_name, artist):
        results = self.spotify.search(
            q=f'track:"{song_name}" artist:"{artist}"', type="track", limit=1
        )
        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["album"]["release_date"]
        return None

    def get_first_release_date(self, row):
        song_name = row["Normalized Name"]
        artists = row["Artists"]
        artist_list = artists.split(", ")
        for artist in artist_list:
            release_date = self.get_release_date_musicbrainz(song_name, artist)
            if release_date:
                return release_date
            release_date = self.get_release_date_spotify(song_name, artist)
            if release_date:
                return release_date
        return None

    def fetch_release_dates_concurrently(self, df):
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_row = {
                executor.submit(self.get_first_release_date, row): row
                for index, row in df.iterrows()
            }
            for future in as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    release_date = future.result()
                    df.at[row.name, "Release Date"] = release_date
                except Exception as exc:
                    print(f"Error fetching data for row {row.name}: {exc}")
        return df
