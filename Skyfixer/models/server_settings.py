from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, String

from Skyfixer.models.sqlalchemy_objects import Base


class ServerSettings(Base):
    server_id = Column(ForeignKey("servers.id"), primary_key=True)

    enable_greetings = Column(Boolean, default=True)
    enable_moderation_logging = Column(Boolean, default=True)
    enable_welcoming = Column(Boolean, default=True)

    server_language = Column(String(20), default='en')
    force_server_language = Column(Boolean, default=False)

    __tablename__ = "servers_settings"
