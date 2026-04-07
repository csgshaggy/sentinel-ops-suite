#!/bin/bash

RDS_HOST="sentinelcybercop.ce9u88wwevvx.us-east-1.rds.amazonaws.com"
RDS_USER="admin"
DB_NAME="sentinelops"
DB_USER="admin"
DB_PASS="WlIZj7oECiyW20Uf9Y4P"
BOOTSTRAP_PATH="/home/ubuntu/sentinel-ops-suite/bootstrap.sql"

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/db-bootstrap-$TIMESTAMP.log"

mkdir -p "$LOG_DIR"

{
echo "=== SentinelOps DB Bootstrap Started at $TIMESTAMP ==="
echo "[INFO] Using RDS host: $RDS_HOST"
echo "[INFO] Checking if database '$DB_NAME' exists..."

# Check DB existence
DB_EXISTS=$(mysql -h "$RDS_HOST" -u "$RDS_USER" -sse \
"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='$DB_NAME'")

if [ "$DB_EXISTS" = "$DB_NAME" ]; then
    echo "[INFO] Database '$DB_NAME' already exists on RDS."
else
    echo "[INFO] Database '$DB_NAME' does not exist. Creating..."
    mysql -h "$RDS_HOST" -u "$RDS_USER" -e \
    "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo "[INFO] Database '$DB_NAME' created on RDS."
fi

# Ensure user exists
echo "[INFO] Ensuring MySQL user '$DB_USER' exists and has privileges..."
mysql -h "$RDS_HOST" -u "$RDS_USER" <<EOF
CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
EOF

echo "[INFO] User '$DB_USER' ensured and privileges applied."

# Run bootstrap SQL
echo "[INFO] Running bootstrap SQL from '$BOOTSTRAP_PATH'..."
mysql -h "$RDS_HOST" -u "$RDS_USER" <<EOF
USE $DB_NAME;
SOURCE $BOOTSTRAP_PATH;
EOF

echo "[INFO] Bootstrap completed successfully."
echo "=== SentinelOps DB Bootstrap Finished ==="

} | tee "$LOG_FILE"

echo "Log saved to: $LOG_FILE"
