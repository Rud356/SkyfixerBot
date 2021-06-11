from discord import Color, Embed, Guild, Member

from Skyfixer.localisation import translator
from Skyfixer.models import ServerMember, User as DBUser


def user_server_info(
    user: Member, user_from_db: DBUser, server: Guild, server_member: ServerMember, language: str
) -> Embed:
    """
    Generates embed with information about user.

    :param user: discord user object.
    :param user_from_db: user model instance that been obtained from db.
    :param server: discord guild object.
    :param server_member: information about user, related to some server, obtained from db.
    :param language: language name to which we translate embed.
    :return: new embed.
    """
    created_at = user.created_at.strftime("%m/%d/%Y | `%H:%M:%S`")
    joined_at = user.joined_at.strftime("%m/%d/%Y | `%H:%M:%S`")

    about_user_embed = Embed(
        title=translator.translate("user_in_server_title", language).safe_substitute(
            user_mention=f"{user.display_name}#{user.discriminator}"
        ),
        color=Color.random()
    )
    about_user_embed.set_thumbnail(url=user.avatar_url)

    # Basic information
    about_user = translator.translate("user_info_for_embed", language).safe_substitute(
        username=user.mention,
        user_id=user.id,
        coins_amount=user_from_db.coins,
        user_created_at=created_at,
        user_language=user_from_db.language
    )
    about_user_embed.add_field(
        name=translator.translate("basic_info_title", language).safe_substitute(),
        inline=False, value=about_user
    )

    # About users avatar
    about_avatar = translator.translate("user_avatar_info", language).safe_substitute(
        avatar_url=user.avatar_url, is_avatar_animated=user.is_avatar_animated()
    )
    about_user_embed.add_field(
        name=translator.translate("users_avatar_info_title", language).safe_substitute(),
        inline=False, value=about_avatar
    )

    # About birthday and age
    if user_from_db.birthday:
        birthday = user_from_db.birthday.strftime("%d/%m/%Y (day, month, year)")
        age = user_from_db.age

    else:
        birthday = translator.translate("birthday_unknown", language).safe_substitute()
        age = translator.translate("age_is_unknown", language).safe_substitute()

    birthday_info = translator.translate("user_birthday_info", language).safe_substitute(
        birthday_date=birthday,
        users_age=age
    )
    about_user_embed.add_field(
        name=translator.translate("user_birthday_info_title", language).safe_substitute(),
        inline=False, value=birthday_info
    )

    # Server related
    server_related = translator.translate("users_server_related_info", language).safe_substitute(
        server_info=server.name,
        exp_amount=server_member.exp,
        level=server_member.level,
        bans_count=server_member.ban_counter,
        kicks_count=server_member.kick_counter,
        joined_at=joined_at
    )
    about_user_embed.add_field(
        name=translator.translate("users_server_related_title", language).safe_substitute(),
        inline=False, value=server_related
    )
    return about_user_embed
