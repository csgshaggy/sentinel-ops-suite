from app.database import Base
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

class PluginCategory(Base):
    __tablename__ = "plugin_categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    plugins = relationship("Plugin", back_populates="category")
