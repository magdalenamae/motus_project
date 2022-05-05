
DROP TABLE IF EXISTS rides;
DROP TABLE IF EXISTS motus_users;

CREATE TABLE motus_users (
	user_id serial PRIMARY KEY,
	username TEXT UNIQUE,
	hash_pw TEXT,
	email TEXT UNIQUE,
	created_on TIMESTAMP DEFAULT NOW(),
 last_login TIMESTAMP 
);

CREATE TABLE rides (
 ride_id serial PRIMARY KEY,
 owner_id INT REFERENCES motus_users (user_id),
 ride_description TEXT,
 ride_start TEXT,
	ride_end TEXT
);


