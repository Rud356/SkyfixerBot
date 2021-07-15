from .info_commands import InfoCommands
from .server_settings_commands import ServerSettingsCommands
from .simple_commands import SimpleCommands
from .user_settings_commands import UserSettingsCommands
from .admin_commands import AdminCommands
from Skyfixer.skyfixer import skyfixer_bot

skyfixer_bot.add_cog(InfoCommands())
skyfixer_bot.add_cog(SimpleCommands())
skyfixer_bot.add_cog(UserSettingsCommands())
skyfixer_bot.add_cog(ServerSettingsCommands())
skyfixer_bot.add_cog(AdminCommands())
