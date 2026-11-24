from contentculture.app import create_app


# Fake database for testing
class FakeDatabase:
    def __init__(self):
        self.lists = []

    def add_list(self, user_id, name, description):
        list_id = len(self.lists) + 1

        self.lists.append({
            "id": list_id,
            "user_id": user_id,
            "name": name,
            "description": description
        })

        return list_id


def test_create_list(monkeypatch):
    app = create_app()
    app.testing = True

    fake_db = FakeDatabase()

    # Replace the real database connection
    monkeypatch.setattr(
        "contentculture.app.get_db",
        lambda: fake_db
    )

    with app.test_client() as client:
        # Pretend the user is logged in
        with client.session_transaction() as session:
            session["user_id"] = 1

        # Send a request to create a list
        response = client.post(
            "/api/lists",
            json={
                "name": "Favorite Horror Movies",
                "description": "Movies I recommend"
            }
        )

    assert response.status_code == 201
    assert response.json["name"] == "Favorite Horror Movies"
    assert len(fake_db.lists) == 1
    assert fake_db.lists[0]["user_id"] == 1


def test_create_list_requires_login(monkeypatch):
    app = create_app()
    app.testing = True

    # No database should be needed for an unauthorized request
    with app.test_client() as client:
        response = client.post(
            "/api/lists",
            json={"name": "My Movies", "description": ""}
        )

    assert response.status_code == 401


def test_create_list_requires_name(monkeypatch):
    app = create_app()
    app.testing = True

    fake_db = FakeDatabase()

    monkeypatch.setattr(
        "contentculture.app.get_db",
        lambda: fake_db
    )

    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 1

        response = client.post(
            "/api/lists",
            json={"name": "", "description": ""}
        )

    assert response.status_code == 400
    assert len(fake_db.lists) == 0


def test_view_own_list(monkeypatch):
    app = create_app()
    app.testing = True

    class FakeDatabase:
        def get_list(self, list_id, user_id):
            if list_id == 1 and user_id == 5:
                return {
                    "id": 1,
                    "name": "Favorite Horror Movies",
                    "description": "My favorite scary movies.",
                    "media": []
                }
            return None

    monkeypatch.setattr(
        "contentculture.app.get_db",
        lambda: FakeDatabase()
    )

    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 5

        response = client.get("/lists/1")

    assert response.status_code == 200
    assert b"Favorite Horror Movies" in response.data


def test_cannot_view_another_users_list(monkeypatch):
    app = create_app()
    app.testing = True

    class FakeDatabase:
        def get_list(self, list_id, user_id):
            return None

    monkeypatch.setattr(
        "contentculture.app.get_db",
        lambda: FakeDatabase()
    )

    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 10

        response = client.get("/lists/1")

    assert response.status_code == 404