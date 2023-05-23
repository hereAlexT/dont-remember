# users

import logging

from flask import Blueprint, jsonify, current_app, request
from models.user import User
from werkzeug.security import check_password_hash
import uuid
from models import db

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/health", methods=["GET"])
def health_check():
    try:
        response_data = {
            "healthy": True,
            "service": "users"
            # todo: health logic
        }
        return jsonify(response_data), 200
    except Exception as e:
        # If there's an error, return a 503 status code indicating the service is not healthy
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"error": "Service is not healthy."}), 500


def authenticate_password(user, password):
    return check_password_hash(user.password, password)


@users_blueprint.route("/signup", methods=["POST"])
def signup():
    """
    Sign up a new user
    :payload: {username: [username], password:[password]}
    :return:{status: 200, message: "Success"}
            {status: 409, message: "User already exist"}
    """
    logging.debug("Handling request for /api/v1/signup")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logging.debug("Missing username or password")
        return jsonify({"status": 400, "message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if user:
        logging.debug("User already exists")
        return jsonify({"status": 409, "message": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    logging.debug("User created successfully")
    return jsonify({"status": 200, "message": "Success"}), 200


@users_blueprint.route("/login", methods=["POST"])
def login():
    """
    :payload: {username: [username], password: [password]}
    :return:{status: 404, message: "User not found"}
            {status: 200, message: "Login success", token: [token]}
            {status: 401, message: "Wrong password"}
    """
    logging.debug("Handling request for /api/v1/login")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logging.debug("Missing username or password")
        return jsonify({"status": 400, "message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        logging.debug("User not found")
        return jsonify({"status": 404, "message": "User not found"}), 404

    if authenticate_password(user, password):
        token = uuid.uuid4().hex
        user.token = token
        user.token_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        db.session.commit()

        logging.debug("Login success")
        return jsonify({
            "status": 200,
            "message": "Login success",
            "token": token
        }), 200
    else:
        return jsonify({"status": 401, "message": "Wrong password"}), 401


@users_blueprint.route("/logout", methods=["POST"])
def logout():
    """
    :payload: {token: [token]}
    :return: {status: 404, message: "Wrong Token"}
             {status: 200, message: "Logout success"}
             {status: 401, message: "Wrong token"}
    """
    logging.debug("Handling request for /api/v1/logout")
    data = request.get_json()
    token = data.get('token')

    if not token:
        logging.debug("Missing token")
        return jsonify({"status": 400, "message": "Missing token"}), 400

    user = User.query.filter_by(token=token).first()

    if not user:
        logging.debug("Wrong token")
        return jsonify({"status": 404, "message": "Wrong token"}), 404

    user.token = None
    user.token_expiration = None
    db.session.commit()
    logging.debug("Logout success")
    return jsonify({"status": 200, "message": "Logout success"}), 200
