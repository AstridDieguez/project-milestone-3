import os
import json
import requests
import random
from wiki import getWikiURL
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = "https://api.themoviedb.org/3"

query_params = {
    "api_key": os.getenv("TMDB_KEY"),
}
def cutOverview(overview):
    max = 85
    if len(overview) > max:
        return overview[0:max] + "..."
    return overview
def movieBasicInfo(movieID):
    MOVIE_URL = "https://api.themoviedb.org/3/movie"
    MOVIE_URL = os.path.join(MOVIE_URL, str(movieID))

    response = requests.get(
        MOVIE_URL,
        params=query_params
    )
    result = response.json()
    # print(result)
    movie_title = result["title"]
    movie_tagline = result["tagline"]

    if(movie_tagline == ""):
        movie_tagline = cutOverview(result["overview"])

    movie_genres = result["genres"]
    movie_poster_path = result["poster_path"]
    movie_date = result["release_date"]

    movie_genres_str = ""
    if (len(movie_genres) > 0):
        for index in range(len(movie_genres) - 1):
            movie_genres_str += movie_genres[index]["name"] + ", "
        movie_genres_str += movie_genres[len(movie_genres) - 1]["name"]

    info = {"movie_title": movie_title, "movie_tagline": movie_tagline,
        "movie_genres": movie_genres_str, "movie_poster_path": movie_poster_path,
        "movie_date": movie_date}

    return info

def getImageURL(path):
    CONFIG_URL = os.path.join(BASE_URL, "configuration")

    response = requests.get(
        CONFIG_URL,
        params=query_params
    )
    
    base_url = response.json()["images"]["base_url"]
    poster_size = response.json()["images"]["poster_sizes"][6]

    return base_url + poster_size + path

def getMovieInfo(movieID):
    basic_info = movieBasicInfo(movieID)
    image_url = getImageURL(basic_info["movie_poster_path"])
    wiki_url = getWikiURL(basic_info["movie_title"])

    return_values = {"movie_title": basic_info["movie_title"], "movie_tagline": basic_info["movie_tagline"],
        "movie_genres": basic_info["movie_genres"], "movie_date": basic_info["movie_date"], "image_url": image_url, 
        "wiki_url": wiki_url}

    return return_values

def matchRegex(query, search, regex):
    movie_ID = None

    for item in search:
        res = re.search(regex, item["title"])

        if (res):
            movie_ID = item["id"]
            break

def getMovieSearch(query):
    SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

    query_params = {
        "api_key": os.getenv("TMDB_KEY"),
        "query": query,
    }

    response = requests.get(
        SEARCH_URL,
        params=query_params
    )

    # print(response.json())
    movie_list = response.json()
    # print(movie_list["results"][0]["id"])
    # print(movie_list["results"][0]["title"])
    # regex = "^" + query + "$"
    # movie_ID = matchRegex(query, movie_list["results"], regex)
    if (movie_list["total_results"] > 0):
        movie_ID = movie_list["results"][0]["id"]
    else:
        movie_ID = None

    return movie_ID
