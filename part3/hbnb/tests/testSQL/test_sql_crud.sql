-- A script that tests the CRUD operations

-- ########## USERS ##########

-- ### Create users ###
INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'0c095bc9-8ac4-4d50-b16b-e3da1e8ea3fb',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	bob@crash.com,
	bob,
	dylan,
	'$2y$10$wTNrdOTbq4ZA3Vbzc1Nh..vzXBJzEmy2pWANeZ2SiQ4bo.NFEY6Ke',
	False
);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'e4f87197-440f-47ae-8a27-1e1f23184be0',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	bon@tranche.com,
	jean,
	bon,
	'$2y$10$UV5BJ0cDYUO2uQWr9SLfb.FfLzkZD475Xl3HENXtXvdcOaoTGLnKy',
	False
);

INSERT INTO users(id, created_at, updated_at, email, first_name, last_name, password, is_admin)
VALUES (
	'3b670ec5-1ff8-4431-8de7-2b646b05bd3b',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	god@almighty.com,
	supreme,
	god, 
	'3b670ec5-1ff8-4431-8de7-2b646b05bd3b',
	True
);

-- ### Read users ###
SELECT * FROM users;

SELECT is_admin from users WHERE is_admin = True;

-- ### Update users ###
UPDATE users SET last_name = 'léponge' WHERE email = 'bob@crash.com';

UPDATE users SET email = 'bon@sandwich.com' WHERE email = 'bon@tranche.com';  -- Should raise an error cause non admin

-- ### Delete users ###
DELETE FROM users WHERE first_name = 'jean';


-- ########## PLACES ##########

-- ### Create Place ###
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
	'1992dcc6-c608-4874-ac01-76d8c58bbd64',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Maison de Campagne',
	"Petite maison cosy pour profiter d'un petit moment sympa",
	250,
	49.6460955,
	2.9596039,
	'0c095bc9-8ac4-4d50-b16b-e3da1e8ea3fb'
);

INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
	'2e039425-2acd-4b87-94de-3336ee838e7e',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Appartement Perdu',
	"Pour retrouver ce qu'on a perdu",
	300,
	18.46667,
	-72.46667,
	'3b670ec5-1ff8-4431-8de7-2b646b05bd3b'
);

INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
	'13840f3f-2cbc-4aeb-97a4-2930da5a3465',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'Loft en bord de Mer',
	"Pour découvrir ce qui s'y cache",
	150,
	47.7083642,
	1.5062706,
	'e4f87197-440f-47ae-8a27-1e1f23184be0'
);

-- ### Read places ###
SELECT * FROM places;

SELECT title FROM places WHERE title LIKE 'Loft%';

-- ### Update places ###
UPDATE places SET description = 'Pour se retrouver' WHERE id = '2e039425-2acd-4b87-94de-3336ee838e7e';

UPDATE places SET latitude = -2.3291805, longitude = -79.4009307 WHERE title = 'Loft en bord de Mer';

-- ### Delete places ###
DELETE FROM places WHERE title = 'Maison de Campagne';


-- ########## AMENITIES ##########

-- ### Create amenities ###
INSERT INTO amenities(id, created_at, updated_at, name)
VALUES 
('0d1ac10f-555d-4198-a2c8-10b8316b51cf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Wifi'),
('cced556f-222c-45e1-a1f9-0c509d2e7550', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Pool'),
('a84ecfd3-2039-437d-8962-9f746e12a474', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'TV'),
('28eb152c-8b71-4f30-b332-1341a76845b1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Barbecue')
('55368917-c233-42bd-b2ed-9f3fb0bf0b89', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Ping pong table');

-- ### Read amenities ###
SELECT * FROM amenities;

SELECT name FROM amenities WHERE name = 'P%';

-- ### Update amenities ###
UPDATE amenities SET name = 'WiFi' WHERE id = '0d1ac10f-555d-4198-a2c8-10b8316b51cf';

UPDATE amenities SET name = 'BBQ' WHERE name = 'Barbecue';

-- ### Delete amenities ###
DELETE FROM amenities WHERE name = 'Ping pong table';


-- ########## REVIEWS ##########

-- ### Create reviews ###
INSERT INTO reviews (id, created_at, updated_at, text, rating, user_id, place_id)
VALUES (
	'2523b067-d964-42fd-b2a6-09738da46130',
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP,
	"On est allé à Perdu mais on n'a rien trouvé",
	3,
	'0c095bc9-8ac4-4d50-b16b-e3da1e8ea3fb',
	'2e039425-2acd-4b87-94de-3336ee838e7e'
);

INSERT INTO reviews (id, created_at, updated_at, text, rating, user_id, place_id)
VALUES (
	'bf1763f8-2696-4b1a-903b-0c55481eb903',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	"On est allé au fond mais on n'a rien trouvé. La prochaine fois, on ira à Perdu",
	2,
	'e4f87197-440f-47ae-8a27-1e1f23184be0',
	'13840f3f-2cbc-4aeb-97a4-2930da5a3465'
);

INSERT INTO reviews (id, created_at, updated_at, text, rating, user_id, place_id)
VALUES (
	'b3e140a7-10aa-46ee-8b66-c3e0ca228f00',
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	"Campagne était bien mais il manque l'avantage de Ville",
	4,
	'0c095bc9-8ac4-4d50-b16b-e3da1e8ea3fb',
	'1992dcc6-c608-4874-ac01-76d8c58bbd64'
);

-- ### Read reviews ###
SELECT * FROM reviews;

SELECT text FROM reviews WHERE text = '%Perdu%';

-- ### Update reviews ###
UPDATE reviews 