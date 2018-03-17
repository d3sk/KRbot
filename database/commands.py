import discord
from .database import db

db.query('''CREATE TABLE IF NOT EXISTS commands (
              guild_id      INTEGER   NOT NULL,
              owner_id      INTEGER   NOT NULL,
              name          TEXT      NOT NULL,
              response      TEXT      NOT NULL
            )''')


def add_command(author: discord.Member, name: str, text: str):
    db.query('INSERT INTO commands ( guild_id, owner_id, name, response ) VALUES ( :guild_id, :author_id, :name, :txt )',
             guild_id=author.guild.id,
             author_id=author.id,
             name=name.lower(),
             txt=text)


def delete_command(guild: discord.Guild, name):
    db.query('DELETE FROM commands WHERE guild_id=:guild_id AND name=:name',
             guild_id=guild.id,
             name=name.lower())


def get_command(guild: discord.Guild, name):
    r = db.query('SELECT response FROM commands WHERE guild_id=:guild_id AND name=:name',
                 guild_id=guild.id,
                 name=name.lower())
    return r[0].response if len(r.all()) > 0 else None


def get_all_guild_command_names(guild: discord.Guild):
    rows = db.query('SELECT name FROM commands WHERE guild_id=:guild_id', guild_id=guild.id)
    return [row.name for row in rows] if len(rows.all()) > 0 else None
