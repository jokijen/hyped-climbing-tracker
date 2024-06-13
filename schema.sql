CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(55) UNIQUE NOT NULL,
    email VARCHAR(55) UNIQUE NOT NULL,
    password TEXT NOT NULL, 
    administrator BOOLEAN DEFAULT FALSE,
    suspended BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE crags (
    id SERIAL PRIMARY KEY,
    crag_name VARCHAR(55) NOT NULL,
    latitude DECIMAL(8,6),
    longitude DECIMAL(9,6),
    crag_description VARCHAR(1000),
    manager VARCHAR(55),
    created_by INTEGER REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE climbs (
    id SERIAL PRIMARY KEY,
    climb_name VARCHAR(55) NOT NULL,
    difficulty VARCHAR(3),
    climb_type VARCHAR(10) CHECK (climb_type in ('boulder', 'DWS', 'sport', 'trad')) NOT NULL,
    climb_description VARCHAR(1000),
    crag_id INTEGER REFERENCES crags(id) NOT NULL,
    manager VARCHAR(55),
    created_by INTEGER REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE sends (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    climb_id INTEGER REFERENCES climbs(id) NOT NULL,
    send_date DATE,
    send_type VARCHAR(10) CHECK (send_type in ('onsight', 'flash', 'send')) NOT NULL,
    review VARCHAR(1000),
    rating INTEGER DEFAULT 0 CHECK (rating >= 0 AND rating <= 3),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE favourite_crags (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    crag_id INTEGER REFERENCES crags(id) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE ticklist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    climb_id INTEGER REFERENCES climbs(id) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    climb_id INTEGER REFERENCES climbs(id) NOT NULL,
    comment VARCHAR(1000),
    created_at TIMESTAMP DEFAULT NOW()
);
