from contentculture import openlibrary, rawg


def test_search_books(monkeypatch):
    # Create a fake response from Open Library
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "docs": [
                    {
                        "key": "/works/OL123W",
                        "title": "Frankenstein",
                        "author_name": ["Mary Shelley"],
                        "first_publish_year": 1818
                    }
                ]
            }

    # Replace the real API request with our fake response
    def fake_get(url, params, timeout):
        return FakeResponse()

    monkeypatch.setattr(openlibrary.requests, "get", fake_get)

    # Search for a book
    results = openlibrary.search_books("Frankenstein")

    assert len(results) == 1
    assert results[0]["title"] == "Frankenstein"


def test_search_games(monkeypatch):
    # Create a fake response from RAWG
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "results": [
                    {
                        "id": 123,
                        "name": "Stardew Valley",
                        "released": "2016-02-26"
                    }
                ]
            }

    # Replace the real API request with our fake response
    def fake_get(url, params, timeout):
        return FakeResponse()

    monkeypatch.setenv("RAWG_API_KEY", "fake-test-key")
    monkeypatch.setattr(rawg.requests, "get", fake_get)

    # Search for a game
    results = rawg.search_games("Stardew Valley")

    assert len(results) == 1
    assert results[0]["name"] == "Stardew Valley"