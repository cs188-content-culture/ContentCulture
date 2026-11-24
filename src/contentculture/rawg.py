import os
import requests


def search_games(query):
    """Search RAWG for video games."""

    url = "https://api.rawg.io/api/games"

    api_key = os.environ["RAWG_API_KEY"]

    params = {
        "key": api_key,
        "search": query,
        "page_size": 5
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["results"]