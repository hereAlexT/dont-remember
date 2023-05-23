import json
import uuid
import os


def append_to_file(_file_name):
    # Load JSON data
    with open(f"./json_data/{_file_name}.json", 'r') as f:
        data = json.load(f)

    # Append to the SQL file
    with open(f"./init-db.sql", 'a') as sql_file:
        # Iterate over the JSON data
        for key, value in data.items():
            if 'meanings' in value:  # Check if 'meanings' key exists
                for meaning in value['meanings']:
                    # Prepare the data for SQL
                    word = {
                        'uuid': str(uuid.uuid4()),  # Generate a new UUID
                        'word': key.replace("'", "''"),
                        'definition': meaning['def'].replace("'", "''"),
                        'speech_part': meaning['speech_part'].replace("'", "''"),
                        'example': meaning.get('example', '').replace("'", "''"),
                        'language_A': 'en-us',  # Set the appropriate language
                        'language_B': 'en-us'  # Set the appropriate language
                    }

                    # Construct the SQL command
                    insert_word = f"INSERT INTO dict (uuid, word, definition, speech_part, example, language_a, language_b) VALUES ('{word['uuid']}', '{word['word']}', '{word['definition']}', '{word['speech_part']}', '{word['example']}', '{word['language_A']}', '{word['language_B']}');\n"

                    # Write the SQL command to the file
                    sql_file.write(insert_word)


# Remove existing file if exists
if os.path.exists("./init-db.sql"):
    os.remove("./init-db.sql")

# Write the initial part of the SQL script to create tables
with open('./init-db.sql', 'w') as sql_file:
    sql_file.write("""-- Create the 'dont-remember' database
CREATE DATABASE dont_remember;
\c dont_remember

-- Create the 'users' table
CREATE TABLE users
(
    uuid               UUID PRIMARY KEY,
    username           VARCHAR(255) NOT NULL UNIQUE,
    password           VARCHAR(255) NOT NULL,
    token              VARCHAR(255),
    token_created_time TIMESTAMP
);

-- Create the 'words' table
CREATE TABLE words
(
    uuid             UUID PRIMARY KEY,
    dic_uuid         UUID NOT NULL,
    user_uuid        UUID NOT NULL,
    last_review_time TIMESTAMP,
    next_review_time TIMESTAMP,
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);

-- Create the 'dic' table
CREATE TABLE dict
(
    uuid        UUID PRIMARY KEY,
    word        VARCHAR(255) NOT NULL,
    definition  TEXT         NOT NULL,
    speech_part VARCHAR(255) NOT NULL,
    example     TEXT         NOT NULL,
    language_a  VARCHAR(255) NOT NULL,
    language_b  VARCHAR(255) NOT NULL
);

CREATE TABLE team
(
    uuid                UUID PRIMARY KEY,
    team_info_uuid UUID NOT NULL,
    user_uuid           UUID NOT NULL,
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);

CREATE TABLE team_info
(
    uuid                UUID PRIMARY KEY,
    name                VARCHAR(255) NOT NULL
);
""")

# For all files in ./data which end with json format, append data to sql file
for file in os.listdir('./json_data'):
    if file.endswith(".json"):
        append_to_file(file[:-5])

# Copy init-db.sql file to ../initdb.d
os.system(f"cp ./init-db.sql ../initdb.d")
