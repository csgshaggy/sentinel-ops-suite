-- ============================================================
-- SentinelOps Bootstrap SQL
-- Creates DB, schema, and seed data
-- ============================================================

-- 1. Create database
CREATE DATABASE IF NOT EXISTS sentinelops
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sentinelops;

-- ============================================================
-- 2. Core Tables
-- ============================================================

CREATE TABLE users (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    username        VARCHAR(100) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE roles (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_roles (
    user_id BIGINT UNSIGNED NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 3. Plugin System
-- ============================================================

CREATE TABLE plugin_categories (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE plugins (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(150) NOT NULL UNIQUE,
    category_id  BIGINT UNSIGNED,
    entrypoint   VARCHAR(255) NOT NULL,
    version      VARCHAR(50) NOT NULL,
    enabled      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES plugin_categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE plugin_settings (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    plugin_id     BIGINT UNSIGNED NOT NULL,
    setting_key   VARCHAR(100) NOT NULL,
    setting_value JSON NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plugin_id) REFERENCES plugins(id) ON DELETE CASCADE,
    UNIQUE(plugin_id, setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 4. Audit Events
-- ============================================================

CREATE TABLE audit_events (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id      BIGINT UNSIGNED NULL,
    action       VARCHAR(150) NOT NULL,
    resource     VARCHAR(150) NOT NULL,
    resource_id  VARCHAR(150),
    ip_address   VARCHAR(45),
    user_agent   VARCHAR(255),
    metadata     JSON,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX (user_id),
    INDEX (action),
    INDEX (resource)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 5. Sessions & Tokens
-- ============================================================

CREATE TABLE sessions (
    id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id        BIGINT UNSIGNED NOT NULL,
    session_token  CHAR(64) NOT NULL UNIQUE,
    ip_address     VARCHAR(45),
    user_agent     VARCHAR(255),
    expires_at     DATETIME NOT NULL,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX (user_id),
    INDEX (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE refresh_tokens (
    id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id            BIGINT UNSIGNED NOT NULL,
    refresh_token      CHAR(64) NOT NULL UNIQUE,
    parent_session_id  BIGINT UNSIGNED,
    revoked            BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at         DATETIME NOT NULL,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    INDEX (user_id),
    INDEX (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 6. Seed Data
-- ============================================================

-- Admin role
INSERT INTO roles (name, description)
VALUES ('admin', 'Full system access')
ON DUPLICATE KEY UPDATE name=name;

-- Default plugin category
INSERT INTO plugin_categories (name, description)
VALUES ('core', 'Core system plugins')
ON DUPLICATE KEY UPDATE name=name;

-- Example plugin
INSERT INTO plugins (name, category_id, entrypoint, version, enabled)
VALUES ('health_check', 1, 'plugins.health:run', '1.0.0', TRUE)
ON DUPLICATE KEY UPDATE name=name;

-- Admin user (password hash placeholder)
INSERT INTO users (email, username, password_hash)
VALUES ('admin@sentinelops.local', 'admin', 'REPLACE_WITH_HASH')
ON DUPLICATE KEY UPDATE email=email;

-- Assign admin role to admin user
INSERT IGNORE INTO user_roles (user_id, role_id)
VALUES (1, 1);

-- ============================================================
-- END OF FILE
-- ============================================================
