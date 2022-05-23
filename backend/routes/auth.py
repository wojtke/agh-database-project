from datetime import timedelta

from bson import ObjectId
from flask import request
import bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from pydantic.error_wrappers import ValidationError

from .. import app, login_manager, users
from ..models.objectid import PydanticObjectId
from ..models.user import User

# https://medium.com/codex/simple-registration-login-system-with-flask-mongodb-and-bootstrap-8872b16ef915
# https://flask-login.readthedocs.io/en/latest/


@login_manager.user_loader
def load_user(user_id):
    user = users.find_one({"_id": PydanticObjectId(user_id)})
    return User(**user) if user else None


@login_manager.unauthorized_handler
def unauthorized():
    return {"message": "Unauthorized"}, 401


@app.route("/login", methods=["POST"])
def login():
    """Log in a user."""
    login = request.json.get("login")
    password = request.json.get("password")

    user = users.find_one({"login": login})
    if user is None:
        return {"message": "User not found"}, 404
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return {"message": "Invalid credentials"}, 401

    login_user(User(**user), duration=timedelta(days=1))
    return {"message": "Logged in successfully."}, 200


@app.route("/signup", methods=["POST"])
def signup():
    """Sign up a user."""

    login = request.json.get("login")
    password1 = request.json.get("password1")
    password2 = request.json.get("password2")

    if users.find_one({"login": login}):
        return {'message': 'There already is a user with that login'}, 400
    if password1 != password2:
        return {'message': 'Passwords do not match'}, 400

    hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())

    # create new user
    cursor = users.find().sort("user_id", -1).limit(1)
    user_id = cursor[0]["user_id"] + 1 if cursor else 1
    print(user_id)
    raw_usr = request.get_json()
    raw_usr["user_id"] = user_id
    raw_usr["password"] = hashed
    try:
        user = User(**raw_usr)
    except ValidationError as e:
        return {"validation error": e.errors()}, 400
    users.insert_one(user.to_bson())
    return {
        "message": "Signed up successfully.",
        "user": user.to_json()
    }, 200


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log out a user."""
    logout_user()
    return {"message": "Logged out."}, 200

