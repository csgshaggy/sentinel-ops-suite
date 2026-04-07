# ================================
# SentinelOps RDS Configuration
# ================================
RDS_HOST="sentinelcybercop.ce9u88wwevvx.us-east-1.rds.amazonaws.com"
RDS_USER="admin"
DB_NAME="sentinelops"
DB_USER="admin"
DB_PASS="WlIZj7oECiyW20Uf9Y4P"
BOOTSTRAP_PATH="sentinel-ops-suite/bootstrap.sql"

# ================================
# Script Targets
# ================================
CHECK_DB=./check-db.sh
CREATE_DB=./create-db-if-missing.sh
CREATE_USER=./create-user.sh
DB_BOOTSTRAP=./db-bootstrap.sh

# ================================
# Make Targets
# ================================

.PHONY: check-db
check-db:
	@echo "Checking if database $(DB_NAME) exists on RDS host $(RDS_HOST)..."
	@bash $(CHECK_DB)

.PHONY: create-db
create-db:
	@echo "Creating database $(DB_NAME) on RDS host $(RDS_HOST) if missing..."
	@bash $(CREATE_DB)

.PHONY: create-user
create-user:
	@echo "Ensuring MySQL user $(DB_USER) exists and has privileges..."
	@bash $(CREATE_USER)

.PHONY: db-bootstrap
db-bootstrap:
	@echo "Running full SentinelOps DB bootstrap on RDS host $(RDS_HOST)..."
	@bash $(DB_BOOTSTRAP)

.PHONY: all
all: check-db create-db create-user db-bootstrap
	@echo "Full SentinelOps RDS provisioning pipeline completed."
