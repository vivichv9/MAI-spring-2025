#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER superset WITH PASSWORD 'superset';
	CREATE DATABASE superset WITH OWNER superset;
	GRANT ALL PRIVILEGES ON DATABASE superset TO superset;
EOSQL