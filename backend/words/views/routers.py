# words
from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from models import db
from models.dic_word import DicWord
from models.user import User
from models.word_list import WordList
import time
from datetime import datetime, timedelta
import uuid

words_blueprint = Blueprint('words', __name__)


def get_curr_timestamp():
    return datetime.fromtimestamp(time.time())


@words_blueprint.route('/health')
def health():
    try:
        response_data = {
            "healthy": True,
            "service": "words"
            # todo: health logic
        }
        return jsonify(response_data), 200
    except Exception as e:
        # If there's an error, return a 503 status code indicating the service is not healthy
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"error": "Service is not healthy."}), 500


@words_blueprint.route('/add_new_word', methods=['POST'])
@jwt_required()
def add_new_word():
    """
    {
        "word": "word",
    }
    :return:
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    word = data.get('word')

    # check the existence of the user in the database
    user = User.query.filter_by(uuid=user_id).first()
    if not user:
        return jsonify({"status": 401, "message": "Invalid Token: User not found"}), 401

    # find the word in DicWord, if exist continue, else return 404
    dic_word = DicWord.query.filter_by(word=word).first()
    if not dic_word:
        return jsonify({"status": 404, "message": "Word not found", "word": word}), 404

    # check if the word is already in the user's word list
    word_list = WordList.query.filter_by(user_uuid=user_id, word=word).first()
    if word_list:
        return jsonify({"status": 409, "message": "Word already in the list"}), 409

    # if the word does not exist, add the word in word_list.
    # the last_review_time = timestamp of now (in sec)
    # the next_review_time = timestamp in 24 hours of now (in sec)
    new_word = WordList(
        uuid=uuid.uuid4(),
        word=word,
        user_uuid=user_id,
        last_review_time=get_curr_timestamp(),
        next_review_time=get_curr_timestamp() + timedelta(hours=24)
    )
    db.session.add(new_word)
    db.session.commit()
    return jsonify({"status": 200, "message": "Word added successfully"}), 200



@words_blueprint.route('/next_word', methods=['GET'])
def next_word():
    # Get token from body
    # Retrive next word
    return 200


@words_blueprint.route('/update_word', methods=['POST'])
def update_word():
    return 200


@words_blueprint.route('/word_history', methods=['GET'])
def word_history():
    return 200
