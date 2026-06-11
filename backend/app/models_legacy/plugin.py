from app.database import Base
from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

class Plugin(Base):
    __tablename__ = "plugins"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    category_id = Column(BigInteger, ForeignKey("plugin_categories.id"), nullable=True)
    entrypoint = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    enabled = Column(Boolean, nullable=False, server_default=text("1"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    category = relationship("PluginCategory", back_populates="plugins")
    settings = relationship("PluginSettings", back_populates="plugin")
