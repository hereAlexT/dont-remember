-- Create the 'dont-remember' database
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
CREATE TABLE dic
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

