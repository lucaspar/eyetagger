#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- If executing on docker, the database and user are already created.
    -- The commands below are left as a reference:
    --CREATE DATABASE $POSTGRES_DB;
    --CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASS';
    ALTER ROLE $POSTGRES_USER SET client_encoding TO 'utf8';
    ALTER ROLE $POSTGRES_USER SET default_transaction_isolation TO 'read committed';
    ALTER ROLE $POSTGRES_USER SET timezone TO 'America/Indiana/Indianapolis';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL
