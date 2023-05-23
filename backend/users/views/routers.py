# users
import datetime
import logging

from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from models.user import User
from models.team_info import TeamInfo
from models.team_member import TeamMember
from werkzeug.security import check_password_hash, generate_password_hash
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
    new_user = User(uuid=uuid.uuid4(), username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    logging.debug("User created successfully")
    return jsonify({"status": 200, "message": "Success"}), 200


@users_blueprint.route('/token_verify', methods=['POST'])
@jwt_required()
def token_verify():
    # This point will only be reached if the token is valid
    user_id = get_jwt_identity()
    return jsonify({"status": 200, "message": "Token is valid", "user_id": user_id}), 200


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
        expires = datetime.timedelta(hours=1)
        # token = create_access_token(identity=username, expires_delta=expires)
        # create a token with identity = user's uuid
        token = create_access_token(identity=user.uuid, expires_delta=expires)

        logging.debug("Login success")
        return jsonify({
            "status": 200,
            "message": "Login success",
            "token": token
        }), 200
    else:
        return jsonify({"status": 401, "message": "Wrong password"}), 401


@users_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    By using jwt, we don't need logout in serverside

    :payload: {token: [token]}
    :return: {status: 404, message: "Wrong Token"}
             {status: 200, message: "Logout success"}
             {status: 401, message: "Wrong token"}
    """
    return jsonify({"status": 200, "message": "Logout success"}), 200
    # logging.debug("Handling request for /api/v1/logout")
    # data = request.get_json()
    # token = data.get('token')
    #
    # if not token:
    #     logging.debug("Missing token")
    #     return jsonify({"status": 400, "message": "Missing token"}), 400
    #
    # user = User.query.filter_by(token=token).first()
    #
    # if not user:
    #     logging.debug("Wrong token")
    #     return jsonify({"status": 404, "message": "Wrong token"}), 404
    #
    # user.token = None
    # user.token_expiration = None
    # db.session.commit()
    # logging.debug("Logout success")
    # return jsonify({"status": 200, "message": "Logout success"}), 200


@users_blueprint.route("/new_team", methods=["POST"])
@jwt_required()
def new_team():
    """
    1. add an entry in team_info
    2. add my uuid to team_member

    :return:
    """

    try:
        # get the json content
        data = request.get_json()
        name = data.get('name')
        plan = data.get('plan')

        # add a new entry in team_info
        # {uuid, name, plan}
        _new_team = TeamInfo(uuid=uuid.uuid4(), name=name, plan=plan)
        db.session.add(_new_team)
        db.session.commit()

        user_id = get_jwt_identity()
        # add my uuid to team_member
        # {uuid, team_uuid, user_uuid}
        _new_team_member = TeamMember(uuid=uuid.uuid4(), team_uuid=_new_team.uuid, user_uuid=user_id)
        db.session.add(_new_team_member)
        db.session.commit()

        return jsonify({"status": 200, "message": "Success"}), 200
    except Exception as e:
        logging.debug("Error: {}".format(e))
        return jsonify({"status": 400, "message": "Error: {}".format(e)}), 400


@users_blueprint.route("/add_me_to_team", methods=["POST"])
def add_me_to_team():
    return 200


@users_blueprint.route("/update_team", methods=["POST"])
def update_team():
    """
    update study plan:
    :return:
    """
    return 200


# delete team
@users_blueprint.route("/delete_team", methods=["POST"])
def delete_team():
    """
    every member can delete it
    :return:
    """
    return 200


@users_blueprint.route("/team_info", methods=["GET"])
def team_info():
    """
    :return:
     team number and everyone's proges
    {
     "team_name": "team1",
     "team_id": "123",
        "team_member": [
            {
                "username": "user1",
                "progress": 0.5
            },
            {
                "username": "user2",
                "progress": 0.5
            }
    }
    """
    return 200
