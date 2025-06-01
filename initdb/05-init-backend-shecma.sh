#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "backend" --dbname "backend" <<-EOSQL
    CREATE TABLE "users" (
    "user_id" UUID PRIMARY KEY,
    "first_name" text,
    "last_name" text,
    "age" int,
    "email" text,
    "registration_dttm" timestamp,
    "password_hash" text,
    "is_active" BOOLEAN,
    "is_superuser" BOOLEAN,
    "is_verified" BOOLEAN,
    "updated_at" timestamp DEFAULT NOW()
    );

    CREATE TABLE "user_credentials" (
    "user_id" UUID PRIMARY KEY,
    "password_hash" text,
    is_active BOOLEAN,
    is_superuser BOOLEAN,
    is_verified BOOLEAN 
    );

    CREATE TABLE "tokens" (
    "user_id" UUID PRIMARY KEY,
    "token_hash" VARCHAR(100),
    "expiry_date" timestamp,
    "revoked" BOOLEAN,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE "user_logins" (
    "log_id" serial PRIMARY KEY,
    "user_id" UUID,
    "login_dttm" timestamp,
    "ip_address" INET,
    "user_agent" TEXT,
    "login_status" TEXT,
    "failure_reason" TEXT
    );

    CREATE TABLE "carts" (
    "user_id" UUID PRIMARY KEY,
    "product_ids" integer[]
    );

    CREATE TABLE "products" (
    "product_id" int PRIMARY KEY,
    "price" NUMERIC(12, 2),
    "weight" float,
    "description" text,
    "name" text,
    "discount" float,
    "amount" int
    );

    CREATE TABLE "delivery_times" (
    "product_id" int,
    "pickup_id" int,
    "delivery_hours" int,
    "is_express" boolean,
    PRIMARY KEY ("product_id", "pickup_id")
    );

    CREATE TABLE "pickup_points" (
    "pickup_id" SERIAL PRIMARY KEY,
    "address" JSONB,
    "location" GEOGRAPHY(POINT,4326)
    );

    CREATE TABLE "orders" (
    "order_id" serial PRIMARY KEY,
    "user_id" UUID,
    "product_ids" integer[],
    "product_costs" integer[],
    "order_dttm" timestamp,
    "pickup_id" int,
    "order_type" text
    );

    CREATE TABLE "user_favorites" (
    "user_id" UUID PRIMARY KEY,
    "favorites_ids" integer[]
    );

    CREATE TABLE "premium_users" (
    "user_id" UUID PRIMARY KEY,
    "personal_discount" int
    );

    CREATE TABLE "user_balances" (
    "user_id" UUID,
    "balance" money,
    "valid_from" timestamp,
    "valid_to" timestamp,
    PRIMARY KEY ("user_id", "valid_from")
    );

    CREATE TABLE "user_payments" (
    "user_id" UUID PRIMARY KEY,
    "payment_dttm" timestamp,
    "payment_amount" money
    );

    ALTER TABLE "user_credentials" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "tokens" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "orders" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "premium_users" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "user_favorites" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "delivery_times" ADD FOREIGN KEY ("pickup_id") REFERENCES "pickup_points" ("pickup_id");

    ALTER TABLE "delivery_times" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("product_id");

    ALTER TABLE "orders" ADD FOREIGN KEY ("pickup_id") REFERENCES "pickup_points" ("pickup_id");

    ALTER TABLE "carts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "user_logins" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "user_balances" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

    ALTER TABLE "user_payments" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");
EOSQL