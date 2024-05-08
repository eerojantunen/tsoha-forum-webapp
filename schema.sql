CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    tier INTEGER
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    thread_id INTEGER,
    user_id INTEGER,
    status INTEGER,
    created_at TIMESTAMP
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic_name TEXT,
    access_type INTEGER,
    status INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    thread_name TEXT,
    topic_id INTEGER,
    access_type INTEGER,
    status INTEGER,
    creator_id INTEGER
);

CREATE TABLE private_topics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    topic_id INTEGER
);