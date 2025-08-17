'''
part3_similar_actors_genre.py
PART 2: SIMILAR ACTORS BY GENRE

Using the imdb_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- Example: Chris Hemsworth, actor ID “nm1165110”
- Use sklearn.metrics.DistanceMetric to calculate distances
- Output a CSV containing the top ten actors most similar to your query actor
'''

import os
import pandas as pd
import json
from sklearn.metrics import DistanceMetric
from datetime import datetime

def run_similar_actors():
    """Find top-10 most similar actors to Chris Hemsworth (nm1165110)."""

    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'imdb_movies_clean.json')
    df = pd.read_json(data_path, lines=True)

    rows = []
    for _, row in df.iterrows():
        # Ensure genres is a list
        genres = row.get("genres", [])
        if isinstance(genres, str):
            try:
                genres = json.loads(genres)
            except:
                genres = []

        # Ensure actors is a list
        actors = row.get("actors", [])
        if isinstance(actors, str):
            try:
                actors = json.loads(actors)
            except:
                actors = []

        # Safely iterate actors
        for actor in actors:
            if isinstance(actor, (list, tuple)) and len(actor) == 2:
                actor_id, actor_name = actor
                for genre in genres:
                    rows.append({
                        "actor_id": actor_id,
                        "actor_name": actor_name,
                        "genre": genre
                    })
            else:
                # Skip malformed entries
                continue

    df_long = pd.DataFrame(rows)

    # Pivot to actor x genre
    actor_genre = df_long.pivot_table(
        index=["actor_id", "actor_name"],
        columns="genre",
        aggfunc=len,
        fill_value=0
    )

    # Feature matrix
    X = actor_genre.values

    # Distance metrics
    cosine = DistanceMetric.get_metric("cosine")
    euclidean = DistanceMetric.get_metric("euclidean")

    actor_index = actor_genre.index.get_loc(("nm1165110", "Chris Hemsworth"))
    query_vec = X[actor_index:actor_index+1]

    cos_distances = cosine.pairwise(query_vec, X)[0]
    euc_distances = euclidean.pairwise(query_vec, X)[0]

    results = pd.DataFrame({
        "actor_id": [i[0] for i in actor_genre.index],
        "actor_name": [i[1] for i in actor_genre.index],
        "cosine_dist": cos_distances,
        "euclidean_dist": euc_distances
    }).sort_values("cosine_dist")

    # Exclude Chris Hemsworth himself
    results = results[results["actor_id"] != "nm1165110"]

    top10 = results.head(10)

    out_name = f"similar_actors_genre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    out_path = os.path.join(os.path.dirname(__file__), '..', 'data', out_name)
    top10.to_csv(out_path, index=False)

    print("Top 10 similar actors to Chris Hemsworth (cosine):")
    print(top10[["actor_name", "cosine_dist"]])
    print("\nHow does this change with Euclidean distance?")
    print(results.sort_values("euclidean_dist").head(10)[["actor_name", "euclidean_dist"]])

    return top10

def __call__():
    return run_similar_actors()