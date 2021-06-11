from discord import Color, Embed, User

from Skyfixer.models import User as DBUser


def user_pm_info(user: User, user_from_db: DBUser) -> Embed:
    """
    Generates embed with information about user.

    :param user: discord user object.
    :param user_from_db: user model instance that been obtained from db.
    :return: new embed.
    """
    created_at = user.created_at.strftime("%m/%d/%Y | `%H:%M:%S`")

    about_user_embed = Embed(
        title=user_from_db.translate_phrase("user_info_in_pm_title").safe_substitute(),
        color=Color.random()
    )
    about_user_embed.set_thumbnail(url=user.avatar_url)

    # About user
    about_user = user_from_db.translate_phrase("user_info_for_embed").safe_substitute(
        username=user.name,
        user_id=user.id,
        coins_amount=user_from_db.coins,
        user_created_at=created_at,
        user_language=user_from_db.language
    )
    about_user_embed.add_field(
        name=user_from_db.translate_phrase("basic_info_title").safe_substitute(),
        inline=False, value=about_user
    )

    # About avatar
    about_avatar = user_from_db.translate_phrase("user_avatar_info").safe_substitute(
        avatar_url=user.avatar_url, is_avatar_animated=user.is_avatar_animated()
    )
    about_user_embed.add_field(
        name=user_from_db.translate_phrase("users_avatar_info_title").safe_substitute(),
        inline=False, value=about_avatar
    )

    # About birthday and age
    if user_from_db.birthday:
        birthday = user_from_db.birthday.strftime("%d/%m/%Y (day, month, year)")
        age = user_from_db.age

    else:
        birthday = user_from_db.translate_phrase("birthday_unknown").safe_substitute()
        age = user_from_db.translate_phrase("age_is_unknown").safe_substitute()

    birthday_info = user_from_db.translate_phrase("user_birthday_info").safe_substitute(
        birthday_date=birthday,
        users_age=age
    )
    about_user_embed.add_field(
        name=user_from_db.translate_phrase("user_birthday_info_title").safe_substitute(),
        inline=False, value=birthday_info
    )

    # About settings
    about_settings = user_from_db.translate_phrase("users_settings").safe_substitute(
        is_hiding_age=user_from_db.hide_age, is_hiding_birthday=user_from_db.hide_birthday
    )
    about_user_embed.add_field(
        name=user_from_db.translate_phrase("users_settings_title").safe_substitute(),
        inline=False, value=about_settings
    )

    return about_user_embed
