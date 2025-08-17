"""
part2_network_centrality.py
PART 2: NETWORK CENTRALITY METRICS

Using the imdb_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Tailor this code scaffolding and its structure to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
"""

import os
import pandas as pd
import networkx as nx
from datetime import datetime

# Build the graph
g = nx.Graph()

# Load the dataset
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'imdb_movies_2000to2022.prolific.json')
df = pd.read_json(data_path, lines=True)

# Iterate through movies and create graph
for _, row in df.iterrows():
    actors = row.get('actors', [])
    for i, (left_actor_id, left_actor_name) in enumerate(actors):
        g.add_node(left_actor_id, name=left_actor_name)
        for right_actor_id, right_actor_name in actors[i+1:]:
            g.add_node(right_actor_id, name=right_actor_name)
            if g.has_edge(left_actor_id, right_actor_id):
                g[left_actor_id][right_actor_id]["weight"] += 1
            else:
                g.add_edge(left_actor_id, right_actor_id, weight=1)

# Print node info
print("Nodes:", len(g.nodes))

# Compute centrality
degree_centrality = nx.degree_centrality(g)
top10 = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 actors by centrality:")
for actor_id, centrality in top10:
    print(g.nodes[actor_id]['name'], centrality)

# Save results to CSV
centrality_df = pd.DataFrame([
    {
        "actor_id": node,
        "actor_name": g.nodes[node]["name"],
        "degree_centrality": degree_centrality[node],
        "degree": g.degree[node],
    }
    for node in g.nodes
])

out_name = f"network_centrality_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
out_path = os.path.join(os.path.dirname(__file__), '..', 'data', out_name)
centrality_df.to_csv(out_path, index=False)
print(f"Centrality CSV saved to {out_path}")

# Callable for main.py
def __call__():
    return centrality_df
