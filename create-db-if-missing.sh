#!/bin/bash

RDS_HOST="sentinelcybercop.ce9u88wwevvx.us-east-1.rds.amazonaws.com"
RDS_USER="admin"
DB_NAME="sentinelops"
DB_USER="admin"
DB_PASS="WlIZj7oECiyW20Uf9Y4P"
BOOTSTRAP_PATH="sentinel-ops-suite/bootstrap.sql"

echo "Checking if database '$DB_NAME' exists on RDS host '$RDS_HOST'..."

DB_EXISTS=$(mysql -h "$RDS_HOST" -u "$RDS_USER" -sse \
"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='$DB_NAME'")

if [ "$DB_EXISTS" = "$DB_NAME" ]; then
    echo "Database '$DB_NAME' already exists on RDS."
else
    echo "Database '$DB_NAME' does not exist. Creating..."
    mysql -h "$RDS_HOST" -u "$RDS_USER" -e \
    "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo "Database '$DB_NAME' created on RDS."
fi
