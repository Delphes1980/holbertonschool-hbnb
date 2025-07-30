-- A script that creates the tables needed by the app and adds some
-- records to those tables.

-- DROP TABLE IF EXISTS place_amenity;
-- DROP TABLE IF EXISTS reviews;
-- DROP TABLE IF EXISTS places;
-- DROP TABLE IF EXISTS amenities;
-- DROP TABLE IF EXISTS users;

CREATE TABLE users(
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

CREATE TABLE places(
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

CREATE TABLE reviews(
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

CREATE TABLE amenities(
	id CHAR(36) PRIMARY KEY NOT NULL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	name VARCHAR(255) NOT NULL,
	UNIQUE(name)
);

CREATE TABLE place_amenity(
	place_id CHAR(36),
	amenity_id CHAR(36),

	FOREIGN KEY (place_id) REFERENCES places(id),
	FOREIGN KEY (amenity_id) REFERENCES amenities(id),
	CONSTRAINT PK_place_amenity PRIMARY KEY (place_id, amenity_id)
);

CREATE TRIGGER update_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER update_places_updated_at
AFTER UPDATE ON places
FOR EACH ROW
BEGIN
    UPDATE places SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER update_reviews_updated_at
AFTER UPDATE ON reviews
FOR EACH ROW
BEGIN
    UPDATE reviews SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER update_amenities_updated_at
AFTER UPDATE ON amenities
FOR EACH ROW
BEGIN
    UPDATE amenities SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
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

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'40a54b25-fc77-4353-94c8-50d882600b86',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'admin@example.com',
	'Admin',
	'User',
	'$2b$12$tqImhttAtUNGQOjPqI5PZ.GFOqkO.owLSJiG16bOtT4LCzmQTaoWG',
	True
	);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'c6eca9ff-cd38-402e-afe2-e24949a4d858',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'deleted@example.com',
	'Deleted',
	'User',
	'$2b$12$KoRE19LjSeh8pAGLYdd9Q.DMMCYs7TH3EYFizvdoyuaX62JFg2TmW',
	False
	);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'6fb5f1c1-f9d4-4987-aee3-16ab71704835',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'john@doe.com',
	'John',
	'Doe',
	'$2b$12$KoRE19LjSeh8pAGLYdd9Q.DMMCYs7TH3EYFizvdoyuaX62JFg2TmW',
	False
	);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'7414383a-c590-41aa-a4a5-02c11b8f2b17',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'jane@doe.com',
	'Jane',
	'Doe',
	'$2b$12$KoRE19LjSeh8pAGLYdd9Q.DMMCYs7TH3EYFizvdoyuaX62JFg2TmW',
	False
	);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'13a9b620-310c-4e3a-846c-9d548fcf240a',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'charles@ingalls.com',
	'Charles',
	'Ingalls',
	'$2a$12$Jf1ZR1o4uO5KI/LdjQdeD.sT6YPXoUgPZyuCjLaYejmiD1lnkUyrW',
	False
	);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'72d605d3-af7b-4055-9fe6-fc01c0e86345',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'big@daddy.com',
	'Big',
	'Daddy',
	'$2a$12$N3/kq/zKvv2jauyTRCZQt./F7szvuOAEU2TOI794EkwVFzV39WGeO',
	False
	);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'c2676497-058b-4438-9aad-e2591186e3d8',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'michael@myers.com',
	'Michael',
	'Myers',
	'$2a$12$6vUthmk9Wezjm1N5uAt4zeT8a3xTcuux/cr.aE/Jr.B.u8XutLw2C',
	False
	);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'dcc28b1a-50ce-4d48-b7dc-1d29094e7d40',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'carrie@bradshaw.com',
	'Carrie',
	'Bradshaw',
	'$2a$12$uPtJWNvSH0QGDQpPJoFndunJrVs9WgAuhqIN0gMB/mnSAatBbPy6u',
	False
);

INSERT INTO amenities(id, created_at, updated_at, name)
VALUES (
	'9505dcd5-2d59-403f-a6da-b818e1db9d55',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'WiFi'
);

INSERT INTO amenities(id, created_at, updated_at, name)
VALUES (
	'2cfb7c28-d405-4856-af63-28d033968df0',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Swimming Pool'
);

INSERT INTO amenities(id, created_at, updated_at, name)
VALUES(
	'a6d13673-416b-4cea-99cc-d846583cfcd1',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Air Conditioning'
);

INSERT INTO amenities(id, created_at, updated_at, name)
VALUES(
	'e400974a-cfb0-4650-beee-96431d3048c7',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Pool'
);

INSERT INTO amenities(id, created_at, updated_at, name)
VALUES(
	'7c30b67a-166f-45e5-87c9-397b4579ad4d',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'BBQ'
);

INSERT INTO amenities(id, created_at, updated_at, name)
VALUES(
	'bae601d4-2ace-4e0b-af9c-8fbf9697bd1e',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Electricity'
);

INSERT INTO amenities(id, created_at, updated_at, name)
VALUES(
	'e6b2beed-e39c-4af0-be40-e266eb8fe6f9',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Balcony'
);

INSERT INTO places(id, title, description, price, 
				   latitude, longitude, owner_id)
VALUES(
	'9962e46f-05fa-4ac2-9617-b53d06713a33',
	'Beautiful apartment',
	'It is an OK place',
	20,
	0,
	0,
	'6fb5f1c1-f9d4-4987-aee3-16ab71704835'
);

INSERT INTO places(id, title, description, price, 
				   latitude, longitude, owner_id)
VALUES(
	'121c0d34-a070-4773-b1bf-b850da8b2607',
	'Bedroom',
	'It is a place to sleep',
	5,
	0,
	0,
	'7414383a-c590-41aa-a4a5-02c11b8f2b17'
);

INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES (
	'1992dcc6-c608-4874-ac01-76d8c58bbd64',
	'"Maison de Campagne"',
	"Cosy little house to enjoy a nice moment",
	250,
	49.6460955,
	2.9596039,
	'6fb5f1c1-f9d4-4987-aee3-16ab71704835'
);

INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES (
	'f428ffc2-b4e3-4117-b393-7ed9df361785',
	'Apartment Perdu',
	"To find what we've lost",
	300,
	18.46667,
	-72.46667,
	'72d605d3-af7b-4055-9fe6-fc01c0e86345'
);

INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES (
	'cb1bcb40-200e-4f60-941a-5fb4e3a15b68',
	'Loft by Mer',
	"To discover what's hidden there",
	150,
	47.7083642,
	1.5062706,
	'13a9b620-310c-4e3a-846c-9d548fcf240a'
);

INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES (
	'44e18cdb-56c6-468e-92ec-edf5d9e69381',
	'Cute little house',
	'Cute little house in the prairy. A beautiful place where you can find yourself.. or nobody.',
	25,
	35.1592256,
	-98.4422802,
	'13a9b620-310c-4e3a-846c-9d548fcf240a'
);

INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES (
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'Modern house',
	'Big modern house with all the comfort you need.',
	150,
	33.76994226292834,
	-118.19424544801036,
	'72d605d3-af7b-4055-9fe6-fc01c0e86345'
);

INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES (
	'21128672-c321-49d0-87d8-b34c76059e02',
	'Cozy Cottage',
	'A charming cottage by the lake',
	75,
	42.3069227,
	-95.0510911,
	'c2676497-058b-4438-9aad-e2591186e3d8'
);

INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES (
	'32d5bab8-599f-47ba-a291-03e5cd3795f9',
	'City Apartment',
	'Spacious apartment near the beach',
	100,
	-22.90172720310348,
	-43.17813365522944,
	'dcc28b1a-50ce-4d48-b7dc-1d29094e7d40'
);

INSERT INTO reviews(id, text, rating, user_id, place_id)
VALUES(
	'8785d826-963b-4294-b67d-3a4b0983e2e5',
	"I didn't like this place at all",
	1,
	'6fb5f1c1-f9d4-4987-aee3-16ab71704835',
	'121c0d34-a070-4773-b1bf-b850da8b2607'
);

INSERT INTO reviews(id, text, rating, user_id, place_id)
VALUES(
	'385fbe4c-34f8-4155-b850-cb1e4bd78a0e',
	"This place was not bad, not great either, but not bad",
	3,
	'7414383a-c590-41aa-a4a5-02c11b8f2b17',
	'9962e46f-05fa-4ac2-9617-b53d06713a33'	
);

INSERT INTO reviews(id, text, rating, user_id, place_id)
VALUES(
	'1f3e3a27-bd8f-42a0-b13e-cc20c3b0034b',
	'I found myself, that was great. Then a deer, that was cool too. And then a bear, i don''t want to go back there again',
	2,
	'dcc28b1a-50ce-4d48-b7dc-1d29094e7d40',
	'44e18cdb-56c6-468e-92ec-edf5d9e69381'
);

INSERT INTO reviews(id, text, rating, user_id, place_id)
VALUES(
	'7afdf57e-5a65-4486-9073-bd71a540208b',
	'Everything you need is in this house, even the things you didn''t know you needed. Best swimming pool ever!',
	5,
	'dcc28b1a-50ce-4d48-b7dc-1d29094e7d40',
	'6afb6d48-82b3-413b-9449-f618469dde8c'
);

INSERT INTO reviews(id, text, rating, user_id, place_id)
VALUES(
	'8d332488-78cd-44c0-8f72-565fa33382fa',
	'The lake was pretty great but sometimes a guy with a hockey mask appears. That''s a little bit scary, but the place was great',
	4,
	'13a9b620-310c-4e3a-846c-9d548fcf240a',
	'21128672-c321-49d0-87d8-b34c76059e02'
);

INSERT INTO reviews(id, text, rating, user_id, place_id)
VALUES(
	'8d3a7e8c-548a-4416-83c8-c907ebbb15b2',
	'The advantage of the city, with its balcony with view to everyone, it''s awesome',
	4,
	'c2676497-058b-4438-9aad-e2591186e3d8',
	'32d5bab8-599f-47ba-a291-03e5cd3795f9'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'9505dcd5-2d59-403f-a6da-b818e1db9d55'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'2cfb7c28-d405-4856-af63-28d033968df0'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'a6d13673-416b-4cea-99cc-d846583cfcd1'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'bae601d4-2ace-4e0b-af9c-8fbf9697bd1e'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'e400974a-cfb0-4650-beee-96431d3048c7'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'7c30b67a-166f-45e5-87c9-397b4579ad4d'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'6afb6d48-82b3-413b-9449-f618469dde8c',
	'e6b2beed-e39c-4af0-be40-e266eb8fe6f9'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'cb1bcb40-200e-4f60-941a-5fb4e3a15b68',
	'9505dcd5-2d59-403f-a6da-b818e1db9d55'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'f428ffc2-b4e3-4117-b393-7ed9df361785',
	'a6d13673-416b-4cea-99cc-d846583cfcd1'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'21128672-c321-49d0-87d8-b34c76059e02',
	'e400974a-cfb0-4650-beee-96431d3048c7'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'21128672-c321-49d0-87d8-b34c76059e02',
	'7c30b67a-166f-45e5-87c9-397b4579ad4d'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'32d5bab8-599f-47ba-a291-03e5cd3795f9',
	'e6b2beed-e39c-4af0-be40-e266eb8fe6f9'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'32d5bab8-599f-47ba-a291-03e5cd3795f9',
	'9505dcd5-2d59-403f-a6da-b818e1db9d55'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'32d5bab8-599f-47ba-a291-03e5cd3795f9',
	'a6d13673-416b-4cea-99cc-d846583cfcd1'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'9962e46f-05fa-4ac2-9617-b53d06713a33',
	'7c30b67a-166f-45e5-87c9-397b4579ad4d'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'9962e46f-05fa-4ac2-9617-b53d06713a33',
	'9505dcd5-2d59-403f-a6da-b818e1db9d55'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'121c0d34-a070-4773-b1bf-b850da8b2607',
	'7c30b67a-166f-45e5-87c9-397b4579ad4d'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'1992dcc6-c608-4874-ac01-76d8c58bbd64',
	'2cfb7c28-d405-4856-af63-28d033968df0'
);

INSERT INTO place_amenity(place_id, amenity_id)
VALUES(
	'1992dcc6-c608-4874-ac01-76d8c58bbd64',
	'7c30b67a-166f-45e5-87c9-397b4579ad4d'
);