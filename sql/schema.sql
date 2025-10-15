CREATE SCHEMA IF NOT EXISTS agency;

CREATE TABLE IF NOT EXISTS agency.organizer (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    "position" VARCHAR(100) NOT NULL,
    work_experience INTEGER CHECK (work_experience >= 0)
);

CREATE TABLE IF NOT EXISTS agency.venue (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    capacity INTEGER CHECK (capacity > 0),
    type VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS agency.artist (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    organizer_id INTEGER REFERENCES agency.organizer(id) ON UPDATE CASCADE ON DELETE CASCADE,
    phone_number VARCHAR(20),
    work_experience INTEGER CHECK (work_experience >= 0)
);

CREATE TABLE IF NOT EXISTS agency.client (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INTEGER CHECK (age >= 0),
    organizer_id INTEGER REFERENCES agency.organizer(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS agency.performance (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTEGER,
    genre VARCHAR(100) NOT NULL,
    number_of_artists INTEGER NOT NULL,
    CONSTRAINT performance_duration_check CHECK (duration > 0)
);

CREATE TABLE IF NOT EXISTS agency.concert_program (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    venue_id INTEGER REFERENCES agency.venue(id) ON UPDATE CASCADE ON DELETE CASCADE,
    duration INTEGER NOT NULL,
    address VARCHAR(100),
    number_of_performances INTEGER NOT NULL,
    "time" VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS agency.ticket (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) NOT NULL UNIQUE,
    price INTEGER NOT NULL CHECK (price >= 0),
    client_id INTEGER REFERENCES agency.client(id) ON UPDATE CASCADE ON DELETE SET NULL,
    concert_program_id INTEGER REFERENCES agency.concert_program(id) ON UPDATE CASCADE ON DELETE CASCADE,
    place VARCHAR(50),
    address VARCHAR(100),
    date DATE NOT NULL,
    "time" VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS agency.test (
    id SERIAL PRIMARY KEY,
    a INTEGER,
    b TEXT
);

CREATE TABLE IF NOT EXISTS agency.artist_performance (
    artist_id INTEGER NOT NULL REFERENCES agency.artist(id) ON UPDATE CASCADE ON DELETE CASCADE,
    performance_id INTEGER NOT NULL REFERENCES agency.performance(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (artist_id, performance_id)
);

CREATE TABLE IF NOT EXISTS agency.organizer_concert_program (
    organizer_id INTEGER NOT NULL REFERENCES agency.organizer(id) ON UPDATE CASCADE ON DELETE CASCADE,
    concert_program_id INTEGER NOT NULL REFERENCES agency.concert_program(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (organizer_id, concert_program_id)
);

CREATE TABLE IF NOT EXISTS agency.performance_concert_program (
    performance_id INTEGER NOT NULL REFERENCES agency.performance(id) ON UPDATE CASCADE ON DELETE CASCADE,
    concert_program_id INTEGER NOT NULL REFERENCES agency.concert_program(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (performance_id, concert_program_id)
);
