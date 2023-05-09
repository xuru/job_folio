#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER root WITH PASSWORD 'root' SUPERUSER CREATEDB;
    SELECT 'CREATE DATABASE exp_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'job_folio');
    GRANT ALL PRIVILEGES ON DATABASE job_folio TO root;
EOSQL
