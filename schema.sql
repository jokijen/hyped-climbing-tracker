CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT, 
    administrator BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP
);
CREATE TABLE crags (
    id SERIAL PRIMARY KEY,
    crag_name TEXT UNIQUE,
    latitude DECIMAL(8,6),
    longitude DECIMAL(9,6),
    crag_description TEXT
);
CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    route_name TEXT,
    crag_id INTEGER REFERENCES crags(id),
    route_type TEXT,
    difficulty TEXT,
    route_description TEXT,
    created_by TEXT REFERENCES users(id),
    created_at TIMESTAMP
);
CREATE TABLE user_climbed (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    route_id INTEGER REFERENCES routes(id),
    sent_at TIMESTAMP,
    review TEXT,
    rating INTEGER,
    created_at TIMESTAMP
);
CREATE TABLE favourite_crags (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    crag_id INTEGER REFERENCES crags(id),
    created_at TIMESTAMP
);
CREATE TABLE ticklist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    route_id INTEGER REFERENCES routes(id),
    created_at TIMESTAMP
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    route_id INTEGER REFERENCES routes(id),
    comment TEXT,
    created_at TIMESTAMP
);
