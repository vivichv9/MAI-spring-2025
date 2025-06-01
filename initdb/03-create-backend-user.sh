#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER backend WITH PASSWORD 'backend';
	CREATE DATABASE backend WITH OWNER backend;
	GRANT ALL PRIVILEGES ON DATABASE backend TO backend;
EOSQL