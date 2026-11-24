# This file should be placed in src/azure_web_app, and should be called db.py
"""Database connection helpers."""

# All of the app's SQL lives in the Database class below. The rest of the app
# calls its methods (db.username_exists(...), db.add_user(...)) and never writes
# SQL itself. If you ever need to change a query, this is the only file to look in.
#
# Each request gets at most one Database. Call get_db() to get it: the first call
# during a request opens a connection, and Flask closes it automatically when the
# request ends. You never need to open or close a connection yourself.

import os
import os.path
import mssql_python
from flask import Flask, g

from ._constants import CONNECTION_STRING_VARIABLE, PACKAGE_ROOT

def get_connection_string() -> str:
    """Read the connection string from the environment"""
    
    # On your laptop, create_app() loads it from your .secret.env file. On Azure,
    # it comes from the environment variable you set in the portal.

    return os.environ[CONNECTION_STRING_VARIABLE]


class Database:
    """One connection to the database, plus a method for every query the app runs."""

    def __init__(self, connection: mssql_python.Connection):
        self.connection = connection

    def close(self) -> None:
        """Close the connection.

        With mssql-python, "closing" actually hands the connection back to the
        driver's built-in connection pool, so the next request can reuse it
        instead of logging in to Azure all over again. Anything that was not
        committed is rolled back.
        """
        self.connection.close()

    def username_exists(self, username: str) -> bool:
        """Return True if a user with this username is already in the database."""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
            return cursor.fetchone() is not None

    def add_user(self, username: str, hashed_password: str, display_name: str) -> bool:
        """Add a new user. Return False if the username is already taken."""
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO Users (username, password, display_name) VALUES (?, ?, ?)",
                    (username, hashed_password, display_name),
                )
            except mssql_python.IntegrityError:
                # Register already checks username_exists first, so how could we
                # get here? If two people register the same name at the same
                # moment, both can pass that check before either INSERT runs. The
                # UNIQUE constraint on the username column catches the second one.
                self.connection.rollback()
                return False
        self.connection.commit()
        return True

    def get_login_info(self, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
        return row if row else None

    def add_list(self, user_id, name, description):
        """Save a new list and return its ID."""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Lists (userid, title, description)
                OUTPUT INSERTED.listid
                VALUES (?, ?, ?)
                """,
                (user_id, name, description)
            )

            list_id = cursor.fetchone()[0]

        self.connection.commit()
        return list_id

    def get_lists(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT listid, title, description
                FROM Lists
                WHERE userid = ?
                ORDER BY listid DESC
                """,
                (user_id,)
            )
            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            }
            for row in rows
        ]

    def get_list(self, list_id, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT listid, title, description
                FROM Lists
                WHERE listid = ? AND userid = ?
                """,
                (list_id, user_id)
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "media": self.get_media(list_id, user_id)
        }


    def add_media(self, list_id, user_id, title, medium, genre, external_id, rating, commentary):
        """Add media to a list owned by the user."""

        with self.connection.cursor() as cursor:

            # Check that the user owns this list
            cursor.execute(
                """
                SELECT listid
                FROM Lists
                WHERE listid = ? AND userid = ?
                """,
                (list_id, user_id)
            )

            if cursor.fetchone() is None:
                return None

            try:
                # Add the media to the Media table
                cursor.execute(
                    """
                    INSERT INTO Media
                        (userid, title, medium, rating, genre, commentary)
                    OUTPUT INSERTED.mediaid
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (user_id, title, medium, rating, genre, commentary)
                )

                media_id = cursor.fetchone()[0]

                # Connect the media to the correct list
                cursor.execute(
                    """
                    INSERT INTO ListItems (listid, mediaid)
                    VALUES (?, ?)
                    """,
                    (list_id, media_id)
                )

                # Save both changes together
                self.connection.commit()

            except Exception:
                self.connection.rollback()
                raise

        return media_id


    def get_media(self, list_id, user_id):
        """Get all media from a list owned by the user."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT Media.mediaid, Media.title, Media.medium, Media.genre,
                    Media.rating, Media.commentary
                FROM ListItems
                JOIN Media ON ListItems.mediaid = Media.mediaid
                JOIN Lists ON ListItems.listid = Lists.listid
                WHERE Lists.listid = ? AND Lists.userid = ?
                ORDER BY ListItems.ID DESC
                """,
                (list_id, user_id)
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "medium": row[2],
                "genre" : row[3],
                "rating": row[4],
                "commentary": row[5]
            }
            for row in rows
        ]
    
def get_db() -> Database:
    """Return this request's Database, connecting on first use."""
    # `g` is Flask's per-request storage (remember it from the API activity?).
    # Anything we put on it disappears when the request ends, so each request
    # gets its own Database, and requests never share one.
    if "db" not in g:
        g.db = Database(mssql_python.connect(get_connection_string()))
    return g.db


def close_db(exception: BaseException | None = None) -> None:
    """Close this request's Database, if the request opened one.

    Flask calls this automatically at the end of every request (see setup_for_app).
    Flask passes in the exception that ended the request (or None), which we
    don't need, but the function still has to accept it.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def setup_for_app(app: Flask) -> None:
    """Hook the database into the app. Call this from create_app()."""
    app.teardown_appcontext(close_db)
