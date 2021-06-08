from discord import Embed

from Skyfixer.localisation import translator
from Skyfixer.skyfixer import SkyfixerBot
from Skyfixer.utils import ttl_cache


@ttl_cache(250)
def generate_about_me(bot: SkyfixerBot, user_language: str) -> Embed:
    bots_name = bot.user.name
    bot_mention = bot.user.mention
    bots_version = bot.__version__
    tech_support_link = "https://discord.gg/2SbVg3SYVd"

    embed = Embed(
        color=0xa049de,
        title=translator.translate("about_me_title", user_language).safe_substitute(),
    )
    embed.set_thumbnail(url=bot.user.avatar_url)

    tech_support = translator.translate("tech_support_here", user_language).safe_substitute()
    embed.add_field(name=tech_support, value=tech_support_link, inline=False)

    facts_about_me_title = translator.translate(
        "facts_about_me_title", user_language
    ).safe_substitute()

    facts_about_me = translator.translate(
        "facts_about_me", user_language
    ).safe_substitute(
        bots_name=bots_name, bot_mention=bot_mention, version=bots_version
    )

    embed.add_field(name=facts_about_me_title, value=facts_about_me, inline=False)

    facts_about_author_title = translator.translate(
        "about_author_title", user_language
    ).safe_substitute()
    facts_about_author = translator.translate(
        "about_author", user_language
    ).safe_substitute()

    embed.add_field(name=facts_about_author_title, value=facts_about_author, inline=False)

    return embed
