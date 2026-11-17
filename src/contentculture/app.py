from dotenv import find_dotenv, load_dotenv
from flask import Flask, abort, render_template, request, session, jsonify
from datetime import datetime
from contentculture import auth, db
from contentculture._constants import SECRET_ENV_FILE


def create_app():
    load_dotenv(find_dotenv(SECRET_ENV_FILE))
    app = Flask(__name__)
    db.setup_for_app(app)
    auth.setup_auth(app)
    setup_routes(app)
    return app

def index():
    return render_template("index.html", name="Flask Bootstrap5")


def show_lists():
    # Preview for "My Lists" using dummy data
    # TODO: Replace sample lists with data from the database.
    # TODO: Restrict this page to logged-in users.
    return render_template("lists.html")


def show_list_details(list_id):
    # Sample data for frontend testing
    # TODO: Replace with database information
    sample_lists = {
        1: {
            "name": "Favorite Horror Movies",
            "description": "My favorite scary movies.",
            "media": [
                {
                    "title": "The Conjuring",
                    "medium": "Movie",
                    "rating": 4,
                    "commentary": "Really creepy."
                },
                {
                    "title": "Nope",
                    "medium": "Movie",
                    "rating": 5,
                    "commentary": "The best!"
                },
                {
                    "title": "Resident Evil",
                    "medium": "Movie",
                    "rating": 5,
                    "commentary": "One of my favorite horror movies."
                }
            ]
        },
        2: {
            "name": "Games I Want to Play",
            "description": "Games on my wishlist.",
            "media": [
                {
                    "title": "Hollow Knight",
                    "medium": "Game",
                    "rating": 5,
                    "commentary": "I want to explore this game."
                },
                {
                    "title": "Stardew Valley",
                    "medium": "Game",
                    "rating": 5,
                    "commentary": "Looks fun and relaxing."
                }
            ]
        },
        3: {
            "name": "Best Books of 2026",
            "description": "Books I enjoyed this year.",
            "media": [
                {
                    "title": "The Hunger Games",
                    "medium": "Book",
                    "rating": 5,
                    "commentary": "A really interesting story."
                },
                {
                    "title": "Frankenstein",
                    "medium": "Book",
                    "rating": 4,
                    "commentary": "Raises interesting questions."
                }
            ]
        }
    }

    selected_list = sample_lists.get(list_id)

    if selected_list is None:
        abort(404)

    return render_template(
        "list_details.html",
        selected_list=selected_list
    )

    # Find the list using its ID
    selected_list = sample_lists.get(list_id)

    # Show an error if the list doesn't exist
    if selected_list is None:
        abort(404)

    return render_template(
        "list_details.html",
        selected_list=selected_list
    )


def setup_routes(app):
    app.route("/")(index)
     # Temporary route for frontend testing.
    app.route("/lists")(show_lists)
    app.route("/lists/<int:list_id>")(show_list_details) 

def run_app(debug: bool = True) -> None:
    app = create_app()
    app.run(debug=debug)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
