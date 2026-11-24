import os
import requests


def search_tv_shows(query):
    # TMDB endpoint for searching TV shows
    url = "https://api.themoviedb.org/3/search/tv"

    # Use our private API token
    token = os.environ["TMDB_READ_ACCESS_TOKEN"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "query": query
    }

    # Request TV show information from TMDB
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    # Return matching TV shows
    return response.json()["results"]


def search_movies(query):
    # TMDB endpoint for searching movies
    url = "https://api.themoviedb.org/3/search/movie"

    # Use our private API token
    token = os.environ["TMDB_READ_ACCESS_TOKEN"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "query": query
    }

    # Request movie information from TMDB
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    # Return the movie search results
    return response.json()["results"]