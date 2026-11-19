"""User registration and login endpoints.

Register is complete. Read through it carefully: the login endpoint you write
at the bottom of this file follows the same pattern.

Notice that there's no SQL in this file. Endpoints decide what should happen;
the Database class in db.py does the talking to the database.
"""

from flask import Flask, request, make_response
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_restful import Api, Resource

from ._constants import (
    BAD_LOGIN_MESSAGE,
    MAX_USERNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
    PASSWORD_PATTERN,
    USERNAME_PATTERN,
)
from .db import get_db

def get_json_body() -> dict:
    """Return the request's JSON body, or an empty dict if there isn't a valid one."""
    # silent=True returns None instead of raising an error when the body
    # isn't JSON, so a bad request gets our 400 instead of a crash.
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def find_missing_field(data: dict, fields: tuple[str, ...]) -> str | None:
    """Return the first field that is missing (or isn't a string), or None if all are present."""
    for field in fields:
        if not isinstance(data.get(field), str):
            return field
    return None


def validate_username(username: str) -> tuple[bool, str]:
    """Check that a username is alphanumeric and at most MAX_USERNAME_LENGTH characters.

    @param username: The username to validate
    @return: A tuple containing a boolean indicating if the username is valid and \
        an invalidation message if it is not (otherwise the empty string)
    """
    if not USERNAME_PATTERN.fullmatch(username):
        return False, f"Username must be alphanumeric and at most {MAX_USERNAME_LENGTH} characters long"
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """Check that a password is at least MIN_PASSWORD_LENGTH characters with no whitespace.

    @param password: The password to validate
    @return: A tuple containing a boolean indicating if the password is valid and \
        an invalidation message if it is not (otherwise the empty string)
    """
    if not PASSWORD_PATTERN.fullmatch(password):
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters with no spaces"
    return True, ""


class Register(Resource):
    def post(self):
        data = get_json_body()

<<<<<<< HEAD
        missing_field = find_missing_field(data, ("username", "password", "display_name"))
=======
        missing_field = find_missing_field(data, ("username", "password", "displayname"))
>>>>>>> prod
        if missing_field is not None:
            return {"message": f"Missing required field: {missing_field}"}, 400

        username = data["username"]
        password = data["password"]
<<<<<<< HEAD
        display_name = data["display_name"].strip()
=======
        display_name = data["displayname"].strip()
>>>>>>> prod

        # Validate everything we can before touching the database.
        is_valid, message = validate_username(username)
        if not is_valid:
            return {"message": message}, 400

        is_valid, message = validate_password(password)
        if not is_valid:
            return {"message": message}, 400

        if not display_name:
            return {"message": "Display name cannot be empty"}, 400

        db = get_db()
        if db.username_exists(username):
            return {"message": "Username already exists"}, 400

        # Hash the password only after the cheaper checks pass. bcrypt is slow on
        # purpose (that's what makes it hard to crack), so we don't want to waste
        # that time on a request we're going to reject.
        hashed_password = generate_password_hash(password).decode("utf-8")

        if not db.add_user(username, hashed_password, display_name):
            return {"message": "Username already exists"}, 400

        return {"message": "User created successfully", "display_name": display_name}, 201

class Login(Resource):
     def post(self):
        data = get_json_body()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": BAD_LOGIN_MESSAGE}, 401

        db = get_db()
        db_data = db.get_login_info(username)

        if db_data is None:
            return {"message": BAD_LOGIN_MESSAGE}, 401

        userid = db_data[0]
        hashed_pwd = db_data[2]
        display_name = db_data[3]

        valid = hashed_pwd is not None and check_password_hash(
            hashed_pwd, password
        )

        if not valid:
            return{"message": BAD_LOGIN_MESSAGE}, 401

        success_message = f"Welcome back, {display_name}!"
        response = make_response({"message": success_message, "display_name": display_name}, 200)

        return response

def setup_auth(app: Flask) -> None:
    """Register the authentication endpoints with the app. Should be called when first creating the flask app"""
    # We create the Api object in here, instead of at the top of the file, so
    # that nothing happens just because someone imported this module.
    api = Api(app)
    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")