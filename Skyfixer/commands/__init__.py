from Skyfixer.skyfixer import skyfixer_bot

from Skyfixer.commands.simple_commands import SimpleCommands
from Skyfixer.commands.user_settings_commands import UserSettingsCommands
from Skyfixer.commands.info_commands import InfoCommands

skyfixer_bot.add_cog(InfoCommands())
skyfixer_bot.add_cog(SimpleCommands())
skyfixer_bot.add_cog(UserSettingsCommands())
