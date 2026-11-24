import requests


def search_books(query):
    """Search Open Library for books."""

    url = "https://openlibrary.org/search.json"

    params = {
        "title": query,
        "fields": "key,title,author_name,first_publish_year",
        "limit": 5
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["docs"]