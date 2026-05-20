-- SentinelOps Seed Data

INSERT INTO users (username, password_hash, email, role)
VALUES
('admin', 'HASHED_PASSWORD_HERE', 'admin@example.com', 'admin'),
('analyst', 'HASHED_PASSWORD_HERE', 'analyst@example.com', 'analyst');

INSERT INTO system_settings (setting_key, setting_value)
VALUES
('system_mode', 'production'),
('alert_threshold', 'high');

INSERT INTO alerts (alert_type, severity, message)
VALUES
('system', 'info', 'System initialized'),
('auth', 'warning', 'Multiple failed login attempts detected');
