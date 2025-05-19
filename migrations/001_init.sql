CREATE SCHEMA personal_account;



CREATE TABLE IF NOT EXIST personal_account.user{
    rating FLOAT NOT NULL DEFAULT 3,
    };

CREATE TABLE IF NOT EXIST personal_account.basket{
    product_id INT NOT NULL
    };

CREATE TABLE IF NOT EXIST personal_account.purchases{
    product_id INT NOT NULL
    };

CREATE TABLE IF NOT EXIST personal_account.recommendations{
    product_id INT NOT NULL,
    personal_sale FLOAT NOT NULL DEFAULT 0
    };
