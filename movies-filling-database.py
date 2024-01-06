import utils 
import pandas as pd
import numpy as np
import hopsworks

def g():
    
    nb_pages = 20
    first_page = 20

    lte_release_date = '2005-12-31'
    gte_release_date = '2005-01-01'

    print(f'Fetching {nb_pages} pages beggining at page {first_page}, form {gte_release_date} to {lte_release_date}.')
    print('------')
    print()

    movies_dict = utils.get_movies_list(lte_release_date, gte_release_date, nb_pages, first_page)
    all_movie_details = []
    for i in range(len(movies_dict)):
        print(f'Extracting features of film {i} ------')
        movie_id = movies_dict[i]['id'] 
        movie_details = utils.extract_features(movie_id)
        if movie_details == -1:
            # We reached the last movie with revenues
            break
        elif not (movie_details is None):
            all_movie_details.append(movie_details)
    movies_df = pd.DataFrame(all_movie_details)

    features = ['budget', 'id', 
              'popularity', 'release_date', 'revenue', 'runtime', 
              'title', 'vote_average', 'vote_count', 'similar_revenues', 
              'crew_popularity', 'top_cast_popularity']

    movies_df = movies_df[features]
    primary_key = 'id'

    movies_df.to_csv(f'movies_{lte_release_date}_{gte_release_date}_{nb_pages}_{first_page}.csv', index=False)

    project = hopsworks.login()
    fs = project.get_feature_store()

    movies_fg = fs.get_or_create_feature_group(
        name="movies",
        version=1,
        primary_key= primary_key, 
        description="Wine dataset with reduced features")
    movies_fg.insert(movies_df)

if __name__ == "__main__":
    g()
