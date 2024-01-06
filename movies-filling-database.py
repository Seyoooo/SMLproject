import utils 
import pandas as pd
import numpy as np
import hopsworks

def g():
    
    nb_pages = 20
    first_page = 20

    lte_release_date = '2020-12-31'
    gte_release_date = '2020-01-01'

    print(f'Fetching {nb_pages} pages beggining at page {first_page}, form {gte_release_date} to {lte_release_date}.')
    print('------')
    print()

    movies_dict = utils.get_movies_list(lte_release_date, gte_release_date, nb_pages, first_page)
    all_movie_details = []
    for i in range(len(movies_dict)):
        print(f'Extracting features of film {i} ------')
        movie_id = movies_dict[i]['id']
        movie_details = utils.get_movie_details(movie_id)

        # As we sort the request by his revenue, we can stop at the first occurence of a film with no revenues.
        if movie_details['revenue'] == 0:
            print('Last film with revenue saved for this request (no need to fetch more pages).')
            break

        # The budget of the film is a super relevant feature, if we do not know the budget, better to ditch out the film
        if movie_details['budget'] > 0:
            # Avg similar films revenues
            movie_details['similar_revenues'] = utils.get_keywords_related_films_average_score(movie_id)
            # Crew popularity
            movie_details['crew_popularity'] = utils.crew_popularity(movie_id)
            # Top10 movie_cast pop
            cast = utils.get_movie_cast(movie_id=movie_id)
            popularities = [person['popularity'] for person in cast['cast']]
            total_popularity = np.sum(np.sort(popularities)[-10:])
            movie_details['top_cast_popularity'] = total_popularity
            # Add the row
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
