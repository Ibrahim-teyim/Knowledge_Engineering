# Knowledge_Engineering

## Running the code

### Environment
To run the code first set up a python environment. You can use conda for this purpose. We use **Python 3.10.14**.
To create the environment you can run the following command:

```zsh
conda create -n "<NAME_OF_THE_ENVIRONMENT>" python=3.10.14
conda activate <NAME_OF_THE_ENVIRONMENT>
```

*NOTE: replace <NAME_OF_THE_ENVIRONMENT> with your prefered env name.*

Do not forget to add:

```python
SPOTIFY_CLIENT_ID = "<YOUR_CLIENT_ID>"
SPOTIFY_CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
```
to a .env file to be able to run `data_creator.py`


### Installing the libraries

To install the required libraries run:

```zsh
pip3 install -r requirements.txt
```


## Naming protocol of the datasets

The datasets should be in the following file format:

```markdown
Knowledge_Engineering/
├─ datasets/
│  ├─ actor_profit.csv
│  ├─ actor_ratings.csv
│  ├─ music_popularity
│  ├─ news.csv
│  ├─ tv.csv
├─ to_edit_datasets/
│  ├─ actor_profit.csv
│  ├─ actor_ratings.csv
│  ├─ news.csv
│  ├─ tv.csv
│  ├─ spotify.csv
```

Where, **to_edit_datasets/** is used for storing the pure data and **datasets** contain the pre-processed and edited data. The pure data can be accessed using the links below:
* [actor_profit.csv](https://www.kaggle.com/datasets/anweshasaha/bollywood-actors-2010s)
* [actor_ratings.csv](https://www.kaggle.com/datasets/mitesh58/bollywood-movie-dataset)
* [news.csv](https://www.kaggle.com/datasets/therohk/india-headlines-news-dataset)
* [tv.csv](https://www.kaggle.com/datasets/shubhamzorc9/-imdbtop-indian-tv-shows)
* [spotify.csv](https://www.kaggle.com/datasets/kanchana1990/popular-spotify-hindi-hits-top-1000)

## Querying the created KG using Blazergraph

Follow [this guide](https://github.com/blazegraph/database/wiki/Quick_Start) to query the graph. `blazergraph.jar` is present in the repo.


## Explanation of the approach

**NOTE:** *check `data_creator.py` and everything under `data_processing/` to fully grasp the context*

This phase designs a pipeline to process and analyze various datasets related to news articles, TV shows, actor performance, and music popularity. The approach is organized into four main stages: Data Collection, Data Pre-Processing, Data Exchange, and Data Sampling. 

### Data Collection

The initial phase involves gathering data from multiple CSV files. These files include information about news, TV shows, actors' financial performance, actor ratings, and music data sourced from Spotify. The data is loaded into a format suitable for analysis using a custom **data loader**, ensuring that each dataset is correctly imported and ready for the next steps.

### Data Pre-Processing

In this phase, the raw data undergoes several transformation steps to prepare it for analysis. The primary tasks include:

1. **Cleaning and Standardizing Data**: Each dataset is cleaned to remove inconsistencies and standardize formats. This involves ensuring dates are correctly formatted, removing irrelevant columns, and handling missing values.
2. **Normalizing Data**: Financial figures, ratings, and popularity metrics are normalized to a consistent scale. This allows for more accurate comparisons and analyses across different datasets.
3. **Enriching Data**: Additional information, such as release dates for music tracks, is fetched using external APIs. This step ensures that all relevant data points are available for analysis.

### Data Exchange

Data exchange focuses on integrating data from different sources and harmonizing them into a cohesive dataset. Key activities in this stage include:

1. **Identifying Key Subjects**: Names of actors, artists, and TV show stars are extracted and compiled from various datasets. This step is crucial for tracking mentions and sentiment in the news dataset.
2. **Processing News Data**: News headlines are analyzed to identify mentions of the key subjects. This involves filtering headlines, counting subject mentions, and assessing the sentiment of each headline.

### Data Sampling

The final stage involves refining the processed data to ensure it is suitable for analysis. This includes:

1. **Removing Duplicates**: Duplicate entries in the news dataset are removed to avoid redundant analysis.
2. **Formatting Dates**: Dates across all datasets are standardized to a uniform format. This facilitates chronological analysis and comparison.
3. **Scaling Ratings and Metrics**: Various numerical values, such as ratings and popularity scores, are scaled to a consistent range. This normalization makes it easier to compare and analyze data across different contexts.
4. **Sampling News Data**: Since the enormous nature of the dataset increased the time to do further operations on the data news data is sampled since 2015. 

Finally these are all piled up together to build a pipeline and the following sequence is built:

```
process_actor_ratings -> process_actor_profit -> process_tv_shows -> process_music_popularity -> extract_subjects -> process_news -> format_dates. 
```

The main point to draw from this pipeline is that we needed the subjects to process the news dataset so we build it up systematically.


## Explanation of the Knowledge Graph

The Knowledge Graph (KG) is a structured representation using RDF (Resource Description Framework) to model the relationships and attributes of entities such as actors, TV shows, films, news articles, and music tracks. RDF enables linking and querying of data across different datasets, providing a unified and interconnected view.

### actor_profit

The `actor_profit` dataset is represented in RDF with entities such as actors (`ex:Actor`) and films (`ex:Film`). Each film entity has properties like `ex:genre`, `ex:gross_profit`, `ex:rating`, and `ex:release_date`. Actors are linked to films they have acted in using the `ex:acted_in` property.

### actor_ratings

The `actor_ratings` dataset is modeled with actor entities (`ex:Actor`) having properties such as `ex:movieCount`, `ex:ratingSum`, `ex:normalizedMovieRank`, `ex:googleHits`, `ex:normalizedGoogleRank`, and `ex:rating`. These properties help in understanding the popularity and performance of actors in the film industry.

### music_popularity

The `music_popularity` dataset includes artist entities (`ex:Artist`) and music entities (`ex:Music`). Each music entity has properties like `ex:popularity`, `ex:artist_name`, `ex:normalized_name`, `ex:release_date`, and `ex:rating_normalized`. Artists are linked to their music tracks using the `ex:performed` property.

### news

The `news` dataset contains news article entities (`ex:News`) with properties such as `ex:publish_date`, `ex:headline_category`, `ex:headline_text`, `ex:mentions`, `ex:sentiment`, and `ex:ratings`. News articles are linked to subject entities (actors/artist) (`ex:Subject`) they mention using the `ex:subject` property. Subjects, in turn, are linked back to the news articles using the `ex:mentioned` property.

### tv

The `tv` dataset represents TV show entities (`ex:TVShow`) with properties like `ex:duration`, `ex:genre`, `ex:rating`, `ex:no_of_ratings`, `ex:no_of_episodes`, `ex:creators`, `ex:reviews_users`, `ex:reviews_critics`, `ex:seasons`, `ex:storyline`, `ex:language`, `ex:release_date`, `ex:score`, and `ex:rating_normalized`. Actors are linked to TV shows they star in using the `ex:acted_in` property.

### Connections between nodes

In the Knowledge Graph, nodes (entities) are interconnected through various RDF properties:

- **Actors and Films**: Actor entities are linked to film entities they have acted in using the `ex:acted_in` property. Film entities have properties such as `ex:genre`, `ex:gross_profit`, `ex:rating`, and `ex:release_date`.
- **Actors and TV Shows**: Actor entities are linked to TV show entities they star in using the `ex:acted_in` property. TV show entities have properties such as `ex:duration`, `ex:genre`, `ex:rating`, `ex:reviews_users`, and `ex:reviews_critics`.
- **Artists and Music**: Artist entities are linked to music entities they have performed using the `ex:performed` property. Music entities have properties such as `ex:popularity`, `ex:release_date`, and `ex:rating_normalized`.
- **News Articles and Subjects**: News article entities are linked to subject entities they mention using the `ex:subject` property, and subjects are linked back to news articles using the `ex:mentioned` property. News articles have properties like `ex:publish_date`, `ex:headline_category`, `ex:mentions`, `ex:sentiment`, and `ex:ratings`.

### Shared properties and their value in the Research Question

Several RDF properties are shared across different datasets, enabling a unified view for analysis:

- **ex:rating**: Used for both film and TV show entities, allowing comparison of performance across different media.
- **ex:release_date**: Applied to films, TV shows, and music entities, enabling chronological analysis of an actor's or artist's career.
- **ex:mentions** and **ex:sentiment**: Found in news articles, providing insights into public perception and media influence on an actor's or artist's popularity.

Finally, although it is outside of the scope of this project, 
- **ex:genre**: Used for both films and TV shows, allowing analysis of an actor's versatility and preference for certain types of roles.


## Queries

### Types of queries

### Correlation of the queries to the Research Question


## Optimization and Databse

### Blazegraph

The team decided to use Blazegraph as the Knowledge Graph turns out to be huge. Blazegraph does further optimization of the knowledge graph and the queries decreasing the runtime by a considerable amount.