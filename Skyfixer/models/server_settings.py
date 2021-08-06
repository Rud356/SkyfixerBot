from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, String

from Skyfixer.models.sqlalchemy_objects import Base


class ServerSettings(Base):
    server_id = Column(ForeignKey("servers.id"), primary_key=True)

    enable_greetings = Column(Boolean, default=True)
    enable_moderation_logging = Column(Boolean, default=True)
    enable_welcoming = Column(Boolean, default=True)
    enable_music_playing = Column(Boolean, default=True)

    server_language = Column(String(20), default='en')
    force_server_language = Column(Boolean, default=False)

    __tablename__ = "servers_settings"
    settings_keys = {
        "enable_greetings", "enable_moderation_logging", "enable_welcoming",
        "force_server_language",
    }
    tuple_of_settings_keys = tuple(sorted(settings_keys))

    def update_setting(self, key: str, value: bool) -> None:
        """
        Sets settings value for one of keys, defined in settings_keys.
        This function doesn't commits any changes.

        :param key: key that we update.
        :param value: new boolean value.
        :return: nothing.
        """
        if key not in self.settings_keys:
            raise KeyError("Invalid setting key")

        if not isinstance(value, bool):
            raise TypeError("This function can only update bool values")

        if value == getattr(self, key):
            raise ValueError("Nothing changed")

        setattr(self, key, value)
