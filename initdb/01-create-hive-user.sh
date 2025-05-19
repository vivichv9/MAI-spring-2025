#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER hive WITH PASSWORD 'hive';
	CREATE DATABASE metastore WITH OWNER hive;
	GRANT ALL PRIVILEGES ON DATABASE metastore TO hive;
EOSQL