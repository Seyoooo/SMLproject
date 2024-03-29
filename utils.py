import pickle
import requests
import json
import numpy as np
import os

def get_api_key(): 
    with open('hopsworks_api_key.txt', 'r') as f:
        key_text = f.read()
    return key_text

def load_headers_dict():
    variable_value = os.getenv('TMDB_API_HEADER')
    if variable_value is None:
        try:
            with open('headers.pkl', 'rb') as f:
                headers_loaded = pickle.load(f)
        except:
            raise KeyError('TMDB header not found')
        return headers_loaded
    else:
        headers_loaded = dict()
        headers_loaded['accept'] = 'application/json'
        headers_loaded['Authorization'] = variable_value
        return headers_loaded


def get_movie_details(movie_id): 
    headers = load_headers_dict()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict


def get_movies_list(lte_rd : str, gte_rd : str, pages : int = 1, first : int = 0):
    headers = load_headers_dict()
    all_results = []
    
    # Check that the range of pages doesn't reach the max number of the request
    url = f"https://api.themoviedb.org/3/discover/movie?page=1&primary_release_date.gte={gte_rd}&primary_release_date.lte={lte_rd}&include_adult=false&include_video=false&language=en-US&sort_by=revenue.desc"
    tt_pages = requests.get(url, headers=headers).json()['total_pages']
    if tt_pages > 500:
        print('---------')
        print('/!\ Number of pages greater than 500!! All films will not be accessible.')
        print(f'Number of pages : {tt_pages}')
        print('---------')
        print()
    if first + pages > tt_pages:
        raise ValueError(f'The request does not have enough pages for this range. Number of page : {tt_pages}.')

    # Fetch all pages
    for i in range(1+first, first+pages+1):
        print(f'Downloading page {i} ------')
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=revenue.desc&page={i}"
        response = requests.get(url, headers=headers)
        response_dict = json.loads(response.text)
        results = response_dict['results']
        all_results.extend(results)

    return all_results


def get_keywords_related_films_average_score(movie_id):
    headers = load_headers_dict()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?language=en-US&page=1&sort_by=popularity.desc"
    response = requests.get(url, headers=headers)

    avg_revenue = list()
    for film in response.json()['results']:
        movie_id = film['id']
        movie_details = get_movie_details(movie_id)
        if 'revenue' in movie_details.keys():
            revenue = movie_details['revenue']
            if revenue > 0:
                avg_revenue.append(revenue)

    if len(avg_revenue) > 0:
        return sum(avg_revenue) / len(avg_revenue)
    else:
        return 0
    

def get_movie_cast(movie_id):
    headers = load_headers_dict()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict


def get_top3_genres_features(genres_list):
    nb = 0
    genres_id = list()
    while len(genres_list) > 0 and nb < 3:
        id = genres_list.pop(0)['id']
        genres_id.append(id)
        nb += 1
    # Complete the 3-uplet with -1 corresponding to no genres
    while len(genres_id) < 3 :
        genres_id.append(-1)
    return genres_id


def crew_popularity(movie_id):
    headers = load_headers_dict()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
    crew_list = requests.get(url, headers=headers).json()['crew']
    peoples = set()
    for p in crew_list:
        if p['job'] in ['Screenplay', 'Director', 'Story', 'Producer', 'Production Manager', 'Executive Producer', 'Casting']:
            # To avoid counting many times the same man
            peoples.add((p['popularity'], p['name']))
    total_pop = 0
    for pop, _ in peoples:
        total_pop += pop
    return total_pop


def get_latest():
    headers = load_headers_dict()
    url = "https://api.themoviedb.org/3/movie/latest?language=en-US"
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

    movie_response_dict = requests.get(url, headers=headers).json()['results'][1]
    print(movie_response_dict)
    return movie_response_dict


def extract_features(movie_id, latest=False):
    movie_details = get_movie_details(movie_id)

    # As we sort the request by his revenue, we can stop at the first occurence of a film with no revenues.
    if not latest and movie_details['revenue'] == 0:
        print('Last film with revenue saved for this request (no need to fetch more pages).')
        return -1

    # The budget of the film is a super relevant feature, if we do not know the budget, better to ditch out the film
    if movie_details['budget'] > 0:
        # Avg similar films revenues
        movie_details['similar_revenues'] = get_keywords_related_films_average_score(movie_id)
        # Crew popularity
        movie_details['crew_popularity'] = crew_popularity(movie_id)
        # Top10 movie_cast pop
        cast = get_movie_cast(movie_id=movie_id)
        popularities = [person['popularity'] for person in cast['cast']]
        total_popularity = np.sum(np.sort(popularities)[-10:])
        movie_details['top_cast_popularity'] = total_popularity
        return movie_details
    else:
        print('Budget missing!')
        return None


def get_latest_not_infered(df):
    id = -1
    headers = load_headers_dict()
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    tt_pages = requests.get(url, headers=headers).json()['total_pages']
    
    for i in range(1, tt_pages+1):
        url = f"https://api.themoviedb.org/3/movie/upcoming?language=en-US&page={i}"
        movies = requests.get(url, headers=headers).json()['results']
        for m in movies:
            if not (m['id'] in df['id'].values):
                features = extract_features(m['id'], latest=True)
                if not (features is None): 
                    return features
    return id
    