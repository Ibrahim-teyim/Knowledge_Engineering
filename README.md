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