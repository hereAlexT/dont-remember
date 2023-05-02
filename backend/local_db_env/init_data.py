import json
import glob
import random
from sqlalchemy import create_engine, text
import uuid
import time

DB_URI = "postgresql://dont-remember-user:dont-remember-pwd@localhost:5432/dont_remember"
engine = create_engine(DB_URI)
# words_len = -1, if you want to insert all the words from the JSON files. or set a number to insert a specific amount of words
words_len = 3000


def process_json_file(file_path, words_per_file):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if words_per_file > 0:
        words_to_insert = random.sample(list(data.items()), min(words_per_file, len(data.items())))
    else:
        words_to_insert = data.items()

    insert_word = text("""
        INSERT INTO dic (uuid, word, definition, speech_part, example, language_a, language_b)
        VALUES (:uuid, :word, :definition, :speech_part, :example, :language_A, :language_B)
    """)

    with engine.connect() as conn:
        trans = conn.begin()  # Begin a new transaction
        try:
            for key, value in words_to_insert:
                for meaning in value['meanings']:
                    word = {
                        'uuid': uuid.uuid4(),  # Generate a new UUID
                        'word': key,
                        'definition': meaning['def'],
                        'speech_part': meaning['speech_part'],
                        'example': meaning.get('example', ''),
                        'language_A': 'en-us',  # Set the appropriate language
                        'language_B': 'en-us'  # Set the appropriate language
                    }
                    conn.execute(insert_word, word)
            trans.commit()  # Commit the transaction
        except Exception as e:
            print(f"Error: {e}")
            trans.rollback()  # Rollback the transaction in case of error


# Get a list of all JSON files in the folder
dic_file_path = "wordset-dictionary/data"
json_files = glob.glob(dic_file_path + '/*.json')

if words_len > 0:
    words_per_file = words_len // len(json_files)
else:
    words_per_file = -1

start_time = time.time()
processed_files = 0

for file in json_files:
    process_json_file(file, words_per_file)
    processed_files += 1
    elapsed_time = time.time() - start_time
    remaining_files = len(json_files) - processed_files
    remaining_time = elapsed_time / processed_files * remaining_files

    print(
        f"Progress: {processed_files}/{len(json_files)} files processed. Estimated time remaining: {remaining_time:.2f} seconds.")
