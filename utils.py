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
        revenue = movie_details['revenue']
        avg_revenue.append(revenue)

    if len(avg_revenue) > 0:
        return sum(avg_revenue) / len(avg_revenue)
    else:
        return 0
    