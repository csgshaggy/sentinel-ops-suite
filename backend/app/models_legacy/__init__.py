# /home/ubuntu/sentinel-ops-suite/backend/app/models/__init__.py
# SentinelOps — SQLAlchemy Model Registry (Clean Final Version)

# Import all ORM models so SQLAlchemy registers them at startup.
# Keep this file minimal to avoid circular imports.

from app.models.user import User
from app.models.session import Session
from app.models.audit_event import AuditEvent
from app.models.plugin import Plugin
from app.models.plugin_category import PluginCategory
from app.models.plugin_settings import PluginSettings
from app.models.user_role import UserRole
from app.models.user_preferences import UserPreferences

__all__ = [
    "User",
    "Session",
    "AuditEvent",
    "Plugin",
    "PluginCategory",
    "PluginSettings",
    "UserRole",
    "UserPreferences",
]
