import discord
from .database import db

db.query('''CREATE TABLE IF NOT EXISTS moderation (
              guild_id          INTEGER   NOT NULL      UNIQUE,
              admin_role_id     INTEGER   DEFAULT NULL,
              moderator_role_id INTEGER   DEFAULT NULL,
              trusted_role_id   INTEGER   DEFAULT NULL,
              mute_role_id      INTEGER   DEFAULT NULL,
              log_channel_id    INTEGER   DEFAULT NULL,
              leave_channel_id  INTEGER   DEFAULT NULL,
              leave_message     TEXT      DEFAULT NULL,
              ghosting_enabled  INTEGER   DEFAULT 1
            )''')


def __guild_is_in_table(guild_id) -> bool:
    r = db.query('SELECT * FROM moderation WHERE guild_id=:guild_id', guild_id=int(guild_id))
    return len(r.all()) > 0


def __add_guild(guild_id: int):
    db.query('INSERT INTO moderation ( guild_id ) VALUES ( :guild_id )', guild_id=int(guild_id))


def get_mod_role_id(guild_id: int):
    r = db.query('SELECT moderator_role_id FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].moderator_role_id if len(r.all()) > 0 else None


def set_mod_role_id(role: discord.Role):
    if not __guild_is_in_table(role.guild.id):
        __add_guild(role.guild.id)
    db.query('UPDATE moderation SET moderator_role_id=:role_id WHERE guild_id=:guild_id',
             role_id=role.id,
             guild_id=role.guild.id)


def get_admin_role_id(guild_id: int):
    r = db.query('SELECT admin_role_id FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].admin_role_id if len(r.all()) > 0 else None


def set_admin_role_id(role: discord.Role):
    if not __guild_is_in_table(role.guild.id):
        __add_guild(role.guild.id)
    db.query('UPDATE moderation SET admin_role_id=:role_id WHERE guild_id=:guild_id',
             role_id=role.id,
             guild_id=role.guild.id)


def get_trusted_role_id(guild_id: int):
    r = db.query('SELECT trusted_role_id FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].trusted_role_id if len(r.all()) > 0 else None


def set_trusted_role_id(role: discord.Role):
    if not __guild_is_in_table(role.guild.id):
        __add_guild(role.guild.id)
    db.query('UPDATE moderation SET trusted_role_id=:role_id WHERE guild_id=:guild_id',
             role_id=role.id,
             guild_id=role.guild.id)


def set_mute_role_id(role: discord.Role):
    if not __guild_is_in_table(role.guild.id):
        __add_guild(role.guild.id)
    db.query('UPDATE moderation SET mute_role_id=:role_id WHERE guild_id=:guild_id',
             role_id=role.id,
             guild_id=role.guild.id)


def get_mute_role_id(guild_id: int):
    r = db.query('SELECT mute_role_id FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].mute_role_id if len(r.all()) > 0 else None


def set_log_channel_id(channel: discord.TextChannel):
    if not __guild_is_in_table(channel.guild.id):
        __add_guild(channel.guild.id)
    db.query('UPDATE moderation SET log_channel_id=:channel_id WHERE guild_id=:guild_id',
             channel_id=channel.id,
             guild_id=channel.guild.id)


def get_log_channel_id(guild_id: int):
    r = db.query('SELECT log_channel_id FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].log_channel_id if len(r.all()) > 0 else None


def set_leave_message(guild: discord.Guild, message: str):
    if not __guild_is_in_table(guild.id):
        __add_guild(guild.id)
    db.query('UPDATE moderation SET leave_message=:message WHERE guild_id=:guild_id',
             message=message,
             guild_id=guild.id)


def get_leave_message(guild_id: int):
    r = db.query('SELECT leave_message FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].leave_message if len(r.all()) > 0 else None


def set_leave_channel_id(channel: discord.TextChannel):
    if not __guild_is_in_table(channel.guild.id):
        __add_guild(channel.guild.id)
    db.query('UPDATE moderation SET leave_channel_id=:channel_id WHERE guild_id=:guild_id',
             channel_id=channel.id,
             guild_id=channel.guild.id)


def get_leave_channel_id(guild_id: int):
    r = db.query('SELECT leave_channel_id FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].leave_channel_id if len(r.all()) > 0 else None


def set_star_channel_id(channel: discord.TextChannel):
    if not __guild_is_in_table(channel.guild.id):
        __add_guild(channel.guild.id)
    db.query('UPDATE moderation SET leave_channel_id=:channel_id WHERE guild_id=:guild_id',
             channel_id=channel.id,
             guild_id=channel.guild.id)


def get_star_channel_id(guild_id: int):
    r = db.query('SELECT star_channel_id FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return r[0].star_channel_id if len(r.all()) > 0 else None


def set_ghosting(enabled: bool, guild_id: int):
    print('ENABLED IS CURRENTLY:', enabled)
    if not __guild_is_in_table(guild_id):
        __add_guild(guild_id)
    db.query('UPDATE moderation SET ghosting_enabled=:enabled WHERE guild_id=:guild_id',
             enabled=int(enabled),
             guild_id=guild_id)


def get_ghosting(guild_id: int):
    if not __guild_is_in_table(guild_id):
        __add_guild(guild_id)
    r = db.query('SELECT ghosting_enabled FROM moderation WHERE guild_id=:guild_id', guild_id=guild_id)
    return bool(r[0].ghosting_enabled) if len(r.all()) > 0 else None
