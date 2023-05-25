# users
import datetime
import logging

from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from models.user import User
from models.team_info import TeamInfo
from models.team_member import TeamMember
from models.word_list import WordList
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from models import db
import traceback

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
        _uuid = uuid.uuid4()
        _new_team = TeamInfo(uuid=_uuid, name=name, plan=plan)
        db.session.add(_new_team)
        db.session.commit()

        user_id = get_jwt_identity()
        # add my uuid to team_member
        # {uuid, team_uuid, user_uuid}
        _new_team_member = TeamMember(uuid=uuid.uuid4(), team_uuid=_new_team.uuid, user_uuid=user_id)
        db.session.add(_new_team_member)
        db.session.commit()

        return jsonify({"status": 200,
                        "message": "Success",
                        "team_uuid": str(_uuid)}), 200
    except Exception as e:
        traceback.print_exc()
        logging.debug("Error: {}".format(e))
        return jsonify({"status": 400, "message": "Error: {}".format(e)}), 400


@users_blueprint.route("/add_me_to_team", methods=["POST"])
@jwt_required()
def add_me_to_team():
    """
    add me to a team
    {
        "team_uuid": [UUID]
    }
    :return:
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        team_uuid = data.get('team_uuid')

        # add a new entry in team_memember
        # {uuid, team_uuid, user_uuid}
        _new_team_member = TeamMember(uuid=uuid.uuid4(), team_uuid=team_uuid, user_uuid=user_id)
        db.session.add(_new_team_member)
        db.session.commit()

        return jsonify({"status": 200, "message": "Success"}), 200
    except Exception as e:
        logging.debug("Error: {}".format(e))
        return jsonify({"status": 400, "message": "Error: {}".format(e)}), 400


@users_blueprint.route("/leave_team", methods=["POST"])
@jwt_required()
def leave_team():
    """
    {
        "team_uuid": [UUID]
    }
    :return:
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        team_uuid = data.get('team_uuid')

        # delete the entry in team_member
        # {uuid, team_uuid, user_uuid}
        _team_member = TeamMember.query.filter_by(team_uuid=team_uuid, user_uuid=user_id).first()
        db.session.delete(_team_member)
        db.session.commit()
        return jsonify({"status": 200, "message": "Success"}), 200
    except Exception as e:
        logging.debug("Error: {}".format(e))
        return jsonify({"status": 400, "message": "Error: {}".format(e)}), 400


@users_blueprint.route("/update_team", methods=["POST"])
@jwt_required()
def update_team():
    """
    :payload:
    {
        "team_uuid": [UUID],
        "plan": [plan,int]
    }
    :return:
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        study_plan = data.get('plan')
        team_uuid = data.get('team_uuid')

        # update the entry in team_info
        # {uuid, name, plan}
        _team_info = TeamInfo.query.filter_by(uuid=team_uuid).first()
        _team_info.plan = study_plan
        db.session.commit()
        return jsonify({"status": 200, "message": "Success"}), 200
    except Exception as e:
        logging.debug("Error: {}".format(e))
        return jsonify({"status": 400, "message": "Error: {}".format(e)}), 400


@users_blueprint.route("/team_info", methods=["GET"])
@jwt_required()
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
                "studied_today: 1,
            },
            {
                "username": "user2",
                "studied_today: 2,
            }
    }
    """
    try:
        # get my current_team from team_member
        user_id = get_jwt_identity()
        _team_member = TeamMember.query.filter_by(user_uuid=user_id).first()

        team_uuid = _team_member.team_uuid

        # get team_name from team_info
        _team_info = TeamInfo.query.filter_by(uuid=team_uuid).first()
        team_name = _team_info.name
        team_plan = _team_info.plan

        # get the team members from team_member
        _team_members = TeamMember.query.filter_by(team_uuid=team_uuid).all()
        team_members_info = []
        for _team_member in _team_members:
            # get the user info from user
            studied_today = check_num_of_words_studied_today(_team_member.user_uuid)
            username = User.query.filter_by(uuid=_team_member.user_uuid).first().username
            team_members_info.append({
                "username": username,
                "studied_today": studied_today
            })

        output_data = {
            "status": 200,
            "team_name": team_name,
            "team_uuid": team_uuid,
            "plan": team_plan,
            "team_member": team_members_info
        }
        return jsonify(output_data), 200
    except Exception as e:
        logging.debug("Error: {}".format(e))
        return jsonify({"status": 400, "message": "Error: {}".format(e)}), 400


@users_blueprint.route("/personal_progress", methods=["GET"])
@jwt_required()
def personal_progres():
    """
    check personal progress
    :return: {
    "status": 200,
    "studied_today": 10,
    "plan": 20,
    }
    """
    user_id = get_jwt_identity()
    # get the study plan in user
    _user = User.query.filter_by(uuid=user_id).first()
    study_plan = _user.study_plan

    check_num_of_words_studied_today(user_id)
    output = {
        "status": 200,
        "studied_today": check_num_of_words_studied_today(user_id),
        "plan": study_plan,
    }
    return jsonify(output), 200


def check_num_of_words_studied_today(user_uuid):
    """
    check the number of words studied today
    :param user_uuid:
    :return:
    """
    today = datetime.date.today()
    return db.session.query(WordList).filter(WordList.user_uuid == user_uuid,
                                             WordList.last_review_time == today).count()
