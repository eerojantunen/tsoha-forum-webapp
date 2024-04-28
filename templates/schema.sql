CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    tier INTEGER
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    status INTEGER,
    thread_id INTEGER,
    user_id INTEGER,
    status INTEGER,
    created_at TIMESTAMP
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    access_type INTEGER,
    status INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER,
    access_type INTEGER,
    status INTEGER
);

CREATE TABLE private_threads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    thread_id INTEGER
);