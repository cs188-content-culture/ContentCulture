from contentculture.app import create_app


class FakeDatabase:
    def __init__(self):
        self.media = []

    def add_media(self, list_id, user_id, title, medium,
                  external_id, rating, commentary):

        if list_id != 1 or user_id != 5:
            return None

        self.media.append({
            "title": title,
            "medium": medium,
            "rating": rating
        })

        return len(self.media)


def test_add_media(monkeypatch):
    app = create_app()
    app.testing = True

    fake_db = FakeDatabase()

    monkeypatch.setattr(
        "contentculture.app.get_db",
        lambda: fake_db
    )

    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 5

        response = client.post(
            "/api/lists/1/media",
            json={
                "title": "The Hunger Games",
                "medium": "Movie",
                "external_id": "70160",
                "rating": 5,
                "commentary": "One of my favorites!"
            }
        )

    assert response.status_code == 201
    assert len(fake_db.media) == 1


def test_add_media_requires_login():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            "/api/lists/1/media",
            json={
                "title": "The Hunger Games",
                "medium": "Movie",
                "rating": 5
            }
        )

    assert response.status_code == 401


def test_cannot_add_to_another_users_list(monkeypatch):
    app = create_app()
    app.testing = True

    monkeypatch.setattr(
        "contentculture.app.get_db",
        lambda: FakeDatabase()
    )

    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 10

        response = client.post(
            "/api/lists/1/media",
            json={
                "title": "The Hunger Games",
                "medium": "Movie",
                "rating": 5
            }
        )

    assert response.status_code == 404