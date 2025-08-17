'''
part1_etl.py
PART 1: ETL the dataset and save in `data/`

Here is the imbd_movie data:
https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true

It is in JSON format, so you'll need to handle accordingly and also figure out what's the best format for the two analysis parts. 
'''

import os
import pandas as pd
import json
import uuid
import requests

def run_etl():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    json_path = os.path.join(data_dir, "imdb_movies.json")
    if not os.path.exists(json_path):
        url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
        r = requests.get(url)
        with open(json_path, "wb") as f:
            f.write(r.content)

    df = pd.read_json(json_path, lines=True)

    # Flatten rating dict
    df["rating_avg"] = df["rating"].apply(lambda x: x.get("avg") if isinstance(x, dict) else None)
    df["rating_votes"] = df["rating"].apply(lambda x: x.get("votes") if isinstance(x, dict) else None)
    df = df.drop(columns=["rating"])

    # Convert list columns to strings for Parquet
    df["actors"] = df["actors"].apply(lambda x: json.dumps(x) if isinstance(x, list) else "[]")
    df["genres"] = df["genres"].apply(lambda x: json.dumps(x) if isinstance(x, list) else "[]")

    # Add unique row IDs
    df["row_id"] = [uuid.uuid4().hex for _ in range(len(df))]

    # Save to multiple formats
    df.to_csv(os.path.join(data_dir, "imdb_movies.csv"), index=False)
    df.to_parquet(os.path.join(data_dir, "imdb_movies.parquet"))
    df.to_json(os.path.join(data_dir, "imdb_movies_clean.json"), orient="records", lines=True)

    print(f"ETL complete. {len(df)} rows saved to /data")
    return df

# This is what main.py will call
def __call__():
    return run_etl()