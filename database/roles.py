import discord

from .database import db

db.query('''CREATE TABLE IF NOT EXISTS roles (
              role_id   INTEGER   NOT NULL, 
              guild_id  INTEGER   NOT NULL, 
              alias     TEXT      NOT NULL
            )''')


def add_role(role: discord.Role, alias: str):
    role_id = role.id
    guild_id = role.guild.id
    alias = role.name if not alias else alias
    db.query('INSERT INTO roles ( role_id, guild_id, alias ) VALUES ( :role_id, :guild_id, :alias )',
             role_id=role_id,
             guild_id=guild_id,
             alias=alias.lower())


def remove_role(role_id):
    db.query('DELETE FROM roles WHERE role_id=:bad_id', bad_id=int(role_id))


def get_from_alias(alias: str, guild_id):
    rows = db.query('SELECT * FROM roles WHERE guild_id=:guild_id AND alias=:alias',
                    alias=str(alias).lower(),
                    guild_id=int(guild_id))

    if not rows.as_dict()[0]:
        return None
    return rows.as_dict()[0].get('role_id')


def get_all_guild_roles(guild_id: int):
    return db.query('SELECT * FROM roles WHERE guild_id=:id', id=guild_id)
