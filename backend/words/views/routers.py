# words
from flask import Blueprint, jsonify, current_app

words_blueprint = Blueprint('words', __name__)


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


@words_blueprint.route('/add_new_word', methods=['POST'])
def add_new_word():
    return 200
