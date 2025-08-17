'''
main.py
You will run this problem set from main.py, so set things up accordingly
'''

import part1_etl as etl
import part2_network_centrality as nc
import part3_similar_actors_genre as sag

# Call functions / instanciate objects from the .py files
def main():

    etl.__call__()  
    nc.__call__()   
    sag.__call__()  

if __name__ == "__main__":
    main()