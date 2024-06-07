CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT, 
    administrator BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE crags (
    id SERIAL PRIMARY KEY,
    crag_name TEXT,
    latitude DECIMAL(8,6),
    longitude DECIMAL(9,6),
    crag_description TEXT,
    created_by TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE climbs (
    id SERIAL PRIMARY KEY,
    climb_name TEXT,
    difficulty TEXT,
    climb_type TEXT,
    climb_description TEXT,
    crag_id INTEGER REFERENCES crags(id),
    created_by TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE user_climbed (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    climb_id INTEGER REFERENCES climbs(id),
    sent_at DATE,
    review TEXT,
    rating INTEGER DEFAULT 0 CHECK (rating >= 0 AND rating <= 3),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE favourite_crags (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    crag_id INTEGER REFERENCES crags(id),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE ticklist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    climb_id INTEGER REFERENCES climbs(id),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    climb_id INTEGER REFERENCES climbs(id),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
