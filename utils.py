import pickle
import requests
import json


def load_headers_dict():
    with open('headers.pkl', 'rb') as f:
        headers_loaded = pickle.load(f)
    return headers_loaded

def get_movie_details(movie_id): 
    headers = load_headers_dict()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict

def get_movies_list(pages : int = 1):
    headers = load_headers_dict()
    all_results = []
    for i in range(1, pages+1):
        print(f'Downloading page {i} ------')
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=revenue.desc&page={i}"
        response = requests.get(url, headers=headers)
        response_dict = json.loads(response.text)
        results = response_dict['results']
        all_results.extend(results)
        # yield response_dict
    # # url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc"
    # url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=revenue.desc"
    # response = requests.get(url, headers=headers)
    # response_dict = json.loads(response.text)
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
