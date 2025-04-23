CREATE SCHEMA IF NOT EXISTS auth;

CREATE TABLE IF NOT EXISTS auth.users(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(200) NOT NULL,
    sex CHAR NOT NULL
);
CREATE TABLE IF NOT EXISTS auth.credentials(
    user_id INT NOT NULL,
    password_hash VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS auth.tokens(
    user_id INT NOT NULL,
    token_hash VARCHAR(100) NOT NULL,
    expiry_date TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(user_id) REFERENCES auth.users(id)
);
