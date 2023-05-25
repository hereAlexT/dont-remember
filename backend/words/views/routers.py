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
        last_review_time=get_curr_timestamp() - timedelta(days=1),
        next_review_time=get_curr_timestamp() + timedelta(minutes=1)
    )
    db.session.add(new_word)
    db.session.commit()
    return jsonify({"status": 200, "message": "Word added successfully"}), 200


@words_blueprint.route('/next_word', methods=['GET'])
@jwt_required()
def next_word():
    """
    Always return the word in the word_list of curr_user with the smallest next_review_time

    :return: {
            "word": word,
            "next_review_time": next_review_time,
            }
    """
    try:
        user_id = get_jwt_identity()

        # check the existence of the user in the database
        user = User.query.filter_by(uuid=user_id).first()
        if not user:
            return jsonify({"status": 401, "message": "Invalid Token: User not found"}), 401

        # find the word in word_list with the smallest next_review_time
        word = WordList.query.filter_by(user_uuid=user_id).order_by(WordList.next_review_time).first()
        if not word:
            return jsonify({"status": 404, "message": "Word not found"}), 404

        return jsonify({
            "status": 200,
            "word": word.word,
            "next_review_time": word.next_review_time,
        }), 200
    except Exception as e:
        current_app.logger.error(f"next_word failed: {e}")
        return jsonify({"error": e}), 500


@words_blueprint.route('/update_word', methods=['PUT'])
@jwt_required()
def update_word():
    """
    update word status for the user. this is not where to update word such as spelling
    {
        "word": word,
        "result": ["remember" | "forget"]
    }
    :return:
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    word = data.get('word')
    result = data.get('result')

    # check the existence of the user in the database
    user = User.query.filter_by(uuid=user_id).first()
    if not user:
        return jsonify({"status": 401, "message": "Invalid Token: User not found"}), 401

    # check if the word is in the user's word list
    word_list = WordList.query.filter_by(user_uuid=user_id, word=word).first()
    if not word_list:
        return jsonify({"status": 404, "message": "Word not found"}), 404

    # update the word_list
    current_time = get_curr_timestamp()
    if result == "remember":
        word_list.last_review_time = current_time
        # next_review_time = current time + (next_review_time - last_review_time) * 2   (in sec)
        word_list.next_review_time = current_time + (
                word_list.next_review_time - word_list.last_review_time) * 2
    elif result == "forget":
        word_list.last_review_time = current_time
        # next_review_time = current time + (next_review_time - last_review_time) * 0.5 (in sec)
        word_list.next_review_time = current_time + (
                word_list.next_review_time - word_list.last_review_time) * 0.5
    else:
        return jsonify({"status": 400, "message": "Invalid result"}), 400

    db.session.commit()
    return jsonify({"status": 200, "message": "Word updated successfully"}), 200


@words_blueprint.route('/delete_word', methods=['POST'])
@jwt_required()
def delete_word():
    """
    payload: {
        "word": word
    }
    :return: 200 if successfully deleted, 404 if word not found
    """

    user_id = get_jwt_identity()
    data = request.get_json()
    word = data.get('word')

    # check the existence of the user in the database
    user = User.query.filter_by(uuid=user_id).first()
    if not user:
        return jsonify({"status": 401, "message": "Invalid Token: User not found"}), 401

    # check if the word is in the user's word list
    word_list = WordList.query.filter_by(user_uuid=user_id, word=word).first()
    if not word_list:
        return jsonify({"status": 404, "message": "Word not found"}), 404

    # delete the word from the word_list
    db.session.delete(word_list)
    db.session.commit()
    return jsonify({"status": 200, "message": "Word deleted successfully"}), 200


@words_blueprint.route('/word_history', methods=['GET'])
@jwt_required()
def word_history():
    """
    :return:  all words in the word list  of current users
    """
    user_id = get_jwt_identity()

    # check the existence of the user in the database
    user = User.query.filter_by(uuid=user_id).first()
    if not user:
        return jsonify({"status": 401, "message": "Invalid Token: User not found"}), 401

    # find all words in word_list of current user
    word_list = WordList.query.filter_by(user_uuid=user_id).all()
    if not word_list:
        return jsonify({"status": 404, "message": "Word not found"}), 404

    """
    if for mat is like {
        "status": 200,
        "history": [ {
        uuid:uuid,
        word: word,
        last_review_time: last_review_time,
        next_review_time: next_review_time,}, ...]
    """
    history = []
    for word in word_list:
        history.append({
            "uuid": word.uuid,
            "word": word.word,
            "last_review_time": word.last_review_time,
            "next_review_time": word.next_review_time,
        })
    return jsonify({
        "status": 200,
        "history": history,
    }), 200
