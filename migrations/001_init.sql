CREATE SCHEMA IF NOT EXISTS products;

CREATE TABLE IF NOT EXISTS products.categories(
    id SERIAL,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS products.products(
    id SERIAL,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    age_category INT,
    quantity INT NOT NULL,
    category_id INT REFERENCES products.categories(id),
    price MONEY NOT NULL
);


CREATE TABLE IF NOT EXISTS products.photos(
    id INT REFERENCES products.products(id),
    photo_url VARCHAR(100) NOT NULL
);