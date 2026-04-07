#!/bin/bash

RDS_HOST="sentinelcybercop.ce9u88wwevvx.us-east-1.rds.amazonaws.com"
RDS_USER="admin"
DB_NAME="sentinelops"
DB_USER="admin"
DB_PASS="WlIZj7oECiyW20Uf9Y4P"
BOOTSTRAP_PATH="sentinel-ops-suite/bootstrap.sql"

echo "Ensuring MySQL user '$DB_USER' exists and has privileges on '$DB_NAME'..."

mysql -h "$RDS_HOST" -u "$RDS_USER" <<EOF
CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
EOF

echo "User '$DB_USER' ensured and privileges applied on RDS."
