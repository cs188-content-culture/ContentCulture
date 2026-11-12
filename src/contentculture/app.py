from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    setup_routes(app)
    return app


def index():
    return render_template("index.html", name="Flask Bootstrap5")


def show_lists():
    # Preview for "My Lists" using dummy data
    # TODO: Replace sample lists with data from the database.
    # TODO: Restrict this page to logged-in users.
    return render_template("lists.html")


def setup_routes(app):
    app.route("/")(index)
     # Temporary route for frontend testing.
    app.route("/lists")(show_lists) 

def run_app(debug: bool = True) -> None:
    app = create_app()
    app.run(debug=debug)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
