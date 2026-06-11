from app.database import Base
from sqlalchemy import Column, BigInteger, String, JSON, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

class PluginSettings(Base):
    __tablename__ = "plugin_settings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    plugin_id = Column(BigInteger, ForeignKey("plugins.id"), nullable=False)
    setting_key = Column(String(100), nullable=False)
    setting_value = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    plugin = relationship("Plugin", back_populates="settings")
