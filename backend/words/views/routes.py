from flask import Blueprint, jsonify
 
api = Blueprint('api', __name__, url_prefix='/api/v1') 

@api.route('/health')
def health():
    return 200

@api.route('/next_word', methods=['GET'])
def next_word():
    # Get token from body
    # Retrive next word
    return 200

@api.route('/update_word', methods=['POST'])
def update_word():
    return 200

@api.route('/word_history', methods=['GET'])
def word_history():
    return 200

@api.route('/add_new_word', methods=['POST'])
def add_new_word():
    return 200
