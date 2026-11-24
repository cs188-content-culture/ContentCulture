from contentculture import tmdb
from contentculture.app import create_app

def test_movie_search_requires_query():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.get("/api/search/movies")

    assert response.status_code == 400
    assert response.json["message"] == "Please enter a movie title."


def test_tv_search_requires_query():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.get("/api/search/tv")

    assert response.status_code == 400
    assert response.json["message"] == "Please enter a TV show name."


# A fake response from TMDB
class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "results": [
                {"id": 70160, "title": "The Hunger Games"}
            ]
        }


def test_search_movies(monkeypatch):
    # Use a test token instead of the real one
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "test-token")

    # Replace the real API request with a fake one
    def fake_get(url, headers, params, timeout):
        assert url.endswith("/search/movie")
        assert params["query"] == "The Hunger Games"
        assert headers["Authorization"] == "Bearer test-token"

        return FakeResponse()

    monkeypatch.setattr(tmdb.requests, "get", fake_get)

    # Test our movie search function
    results = tmdb.search_movies("The Hunger Games")

    assert len(results) == 1
    assert results[0]["title"] == "The Hunger Games"


def test_search_tv_shows(monkeypatch):
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "test-token")

    def fake_get(url, headers, params, timeout):
        assert url.endswith("/search/tv")
        assert params["query"] == "Breaking Bad"

        return FakeResponse()

    monkeypatch.setattr(tmdb.requests, "get", fake_get)

    results = tmdb.search_tv_shows("Breaking Bad")

    assert len(results) == 1