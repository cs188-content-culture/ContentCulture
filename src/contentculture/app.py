from dotenv import find_dotenv, load_dotenv
from flask import Flask, abort, render_template, request, session, jsonify, redirect
from datetime import datetime
from contentculture import auth, db
from contentculture._constants import SECRET_ENV_FILE
from contentculture.tmdb import search_movies, search_tv_shows
from contentculture.db import get_db
from contentculture.openlibrary import search_books
from contentculture.rawg import search_games
import os


def create_app():
    load_dotenv(find_dotenv(SECRET_ENV_FILE))

    app = Flask(__name__)
    app.secret_key = os.environ["FLASK_SECRET_KEY"]

    db.setup_for_app(app)
    auth.setup_auth(app)
    setup_routes(app)
    return app

def index():
    return render_template("index.html", name="Flask Bootstrap5")


def show_lists():
    # Make sure the user is logged in
    user_id = session.get("user_id")

    if user_id is None:
        return redirect("/")

    # Get the user's saved lists
    db = get_db()
    lists = db.get_lists(user_id)

    # Get the user's display name
    display_name = session.get("display_name")

    return render_template(
        "lists.html",
        display_name=display_name,
        lists=lists
    )


def check_session():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"logged_in": False})

    return jsonify({"logged_in": True})


def logout():
    # Forget the logged-in user
    session.clear()

    # Return to the homepage
    return redirect("/")


def show_list_details(list_id):
    # Check whether the user is logged in
    user_id = session.get("user_id")

    if user_id is None:
        return redirect("/")

    # Find the user's list in the database
    db = get_db()
    selected_list = db.get_list(list_id, user_id)

    # Show a 404 if the list doesn't exist or belongs to someone else
    if selected_list is None:
        abort(404)

    return render_template(
        "list_details.html",
        selected_list=selected_list
    )


def search_movie_api():
    # Get the movie title from the URL
    query = request.args.get("query", "").strip()

    # Make sure the user entered something
    if not query:
        return jsonify({"message": "Please enter a movie title."}), 400

    # Search TMDB for matching movies
    movies = search_movies(query)

    return jsonify(movies)


def search_tv_api():
    # Get the TV show name from the URL
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"message": "Please enter a TV show name."}), 400

    # Search TMDB
    shows = search_tv_shows(query)

    return jsonify(shows)


def create_list_api():
    # Make sure the user is logged in
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"message": "Please log in first."}), 401

    # Get the information from the frontend
    data = request.get_json(silent=True) or {}

    name = data.get("name", "")
    description = data.get("description", "")

    # Validate the information
    if not isinstance(name, str) or not isinstance(description, str):
        return jsonify({"message": "Invalid list information."}), 400

    name = name.strip()
    description = description.strip()

    if not name or len(name) > 100 or len(description) > 255:
        return jsonify({"message": "Invalid list name or description."}), 400

    # Save the list to the database
    db = get_db()
    list_id = db.add_list(user_id, name, description)

    return jsonify({
        "message": "List created successfully!",
        "id": list_id,
        "name": name,
        "description": description
    }), 201


def add_media_api(list_id):
    """Add media to one of the user's lists."""

    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"message": "Please log in first."}), 401

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid media information."}), 400

    title = data.get("title")
    medium = data.get("medium")
    external_id = data.get("external_id")
    rating = data.get("rating")
    commentary = data.get("commentary", "")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"message": "Please enter a title."}), 400

    if medium not in ("Movie", "TV Show", "Book", "Game"):
        return jsonify({"message": "Invalid media type."}), 400

    if type(rating) is not int or rating not in range(1, 6):
        return jsonify({"message": "Rating must be between 1 and 5."}), 400

    if not isinstance(commentary, str) or len(commentary) > 255:
        return jsonify({"message": "Commentary is too long."}), 400

    if external_id is not None and not isinstance(external_id, str):
        return jsonify({"message": "Invalid external ID."}), 400

    if len(title.strip()) > 255:
        return jsonify({"message": "Title is too long."}), 400

    if external_id is not None and len(external_id) > 100:
        return jsonify({"message": "External ID is too long."}), 400

    db = get_db()

    media_id = db.add_media(
        list_id,
        user_id,
        title.strip(),
        medium,
        external_id,
        rating,
        commentary
    )

    if media_id is None:
        return jsonify({"message": "List not found."}), 404

    return jsonify({
        "message": "Media added successfully!",
        "id": media_id
    }), 201


def search_book_api():
    """Search Open Library for books."""

    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"message": "Please enter a book title."}), 400

    books = search_books(query)

    return jsonify(books)


def search_game_api():
    """Search RAWG for video games."""

    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"message": "Please enter a game title."}), 400

    games = search_games(query)

    return jsonify(games)


def setup_routes(app):
    app.route("/")(index)
     # Temporary route for frontend testing.
    app.route("/lists")(show_lists)
    app.route("/lists/<int:list_id>")(show_list_details) 
    app.route("/session-check")(check_session)
    app.route("/logout", methods=["POST"])(logout)
    app.route("/api/search/movies")(search_movie_api)
    app.route("/api/search/tv")(search_tv_api)
    app.route("/api/lists", methods=["POST"])(create_list_api)
    app.route("/api/lists/<int:list_id>/media", methods=["POST"])(add_media_api)
    app.route("/api/search/books")(search_book_api)
    app.route("/api/search/games")(search_game_api)

def run_app(debug: bool = True) -> None:
    app = create_app()
    app.run(debug=debug)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
