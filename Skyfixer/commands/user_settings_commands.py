from discord.ext.commands import Cog, command
from sqlalchemy.exc import IntegrityError

from Skyfixer.extended_discord_classes import SkyfixerContext
from Skyfixer.localisation import translator
from Skyfixer.skyfixer import skyfixer_bot


class UserSettingsCommands(Cog):
    """Commands for changing users settings"""
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @command()
    async def set_language(self, ctx: SkyfixerContext, language: str):
        """
        Sets new default language for user that will be used in commands text, invoked by him.
        """
        try:
            await ctx.db_author.set_language(language, session=ctx.session)
            text = ctx.db_author.translate_phrase("new_language_set_successfully").safe_substitute(
                language=language
            )

        except (ValueError, IntegrityError):
            await ctx.session.rollback()
            text = ctx.db_author.translate_phrase("invalid_language").safe_substitute()

        await ctx.send(text)

    @command()
    async def language_list(self, ctx: SkyfixerContext):
        """Shows all available languages."""
        languages_names = list(translator.languages.keys())
        languages_names.append(translator.reference_language.language_name)

        languages_names.sort()
        languages_lines_array = []

        for i in range(0, len(languages_names)+1, 8):
            _ = ", ".join(languages_names[i:i+8])
            languages_lines_array.append(_)

        languages_string = ",\n".join(languages_lines_array)
        text = ctx.db_author.translate_phrase("language_list").safe_substitute(languages=languages_string)
        await ctx.send(text)

    @command()
    async def change_hiding_age(self, ctx: SkyfixerContext):
        """Switches flag that tells if your birthday should be shown or not."""
        await ctx.db_author.change_hiding_age(session=ctx.session)
        showing_or_hiding_age = "hiding" if ctx.db_author.hide_age else "showing"
        text = ctx.db_author.translate_phrase("hiding_age_mode").safe_substitute(
            showing_or_hiding=showing_or_hiding_age
        )
        await ctx.send(text)

    @command()
    async def change_hiding_age(self, ctx: SkyfixerContext):
        """Switches flag that tells if your age should be shown or not."""
        await ctx.db_author.change_hiding_age(session=ctx.session)
        showing_or_hiding_birthday = "hiding" if ctx.db_author.hide_age else "showing"
        text = ctx.db_author.translate_phrase("hiding_birthday_mode").safe_substitute(
            showing_or_hiding=showing_or_hiding_birthday
        )
        await ctx.send(text)

    @command()
    async def set_birthday(self, ctx: SkyfixerContext, birthday_date: str):
        """
        Sets your birthday date by providing birthday date as %d.%m.%Y (day.month.year as numbers).
        Example: {prefix}set_birthday 19.07.1998
        """
        try:
            await ctx.db_author.set_birthday(birthday_date, session=ctx.session)

        except ValueError:
            text = ctx.db_author.translate_phrase("invali_birthday_date").safe_substitute()

        except ctx.db_author.exc.NoTimeTravellersAllowed:
            text = ctx.db_author.translate_phrase("time_traveller_detected").safe_substitute()

        else:
            text = ctx.db_author.translate_phrase("birthday_is_set").safe_substitute(birthday=birthday_date)

        await ctx.send(text)
