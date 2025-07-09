-- A script that create all the tables of the database at the launch of the app

DROP TABLE users;
DROP TABLE places;
DROP TABLE reviews;
DROP TABLE amenities;
DROP TABLE place_amenity;

CREATE TABLE IF NOT EXISTS users(
	id CHAR(36) PRIMARY KEY NOT NULL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE,
	UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS places(
	id CHAR(36) PRIMARY KEY NOT NULL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	title VARCHAR(255) NOT NULL,
	description TEXT,
	price DECIMAL(10, 2) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	owner_id CHAR(36),

	FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reviews(
	id CHAR(36) PRIMARY KEY NOT NULL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	text TEXT NOT NULL,
	rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
	user_id CHAR(36) NOT NULL,
	place_id CHAR(36) NOT NULL,

	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (place_id) REFERENCES places(id),
	UNIQUE(user_id, place_id)
);

CREATE TABLE IF NOT EXISTS amenities(
	id CHAR(36) PRIMARY KEY NOT NULL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	name VARCHAR(255) NOT NULL,
	UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS place_amenity(
	place_id CHAR(36),
	amenity_id CHAR(36),

	FOREIGN KEY (place_id) REFERENCES places(id),
	FOREIGN KEY (amenity_id) REFERENCES amenities(id),
	CONSTRAINT PK_place_amenity PRIMARY KEY (place_id, amenity_id)
);

INSERT OR IGNORE INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'admin@hbnb.io',
	'Admin',
	'HBnB',
	'$2y$10$5Qks2w8WX6UwdrFxZy3dQe2rgy5RU.P6ReQfUgyX9fCDaouxY/El.',
	True
	);

INSERT OR IGNORE INTO amenities(id, created_at, updated_at, name)
VALUES (
	'9505dcd5-2d59-403f-a6da-b818e1db9d55',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'WiFi'
);

INSERT OR IGNORE INTO amenities(id, created_at, updated_at, name)
VALUES (
	'2cfb7c28-d405-4856-af63-28d033968df0',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Swimming Pool'
);

INSERT OR IGNORE INTO amenities(id, created_at, updated_at, name)
VALUES(
	'a6d13673-416b-4cea-99cc-d846583cfcd1',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Air Conditioning'
);