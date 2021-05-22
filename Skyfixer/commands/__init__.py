from Skyfixer.skyfixer import skyfixer_bot

from Skyfixer.commands.simple_commands import SimpleCommands
from Skyfixer.commands.user_settings_commands import UserSettingsCommands

skyfixer_bot.add_cog(SimpleCommands())
skyfixer_bot.add_cog(UserSettingsCommands())
