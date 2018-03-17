import database.moderation
import constants
from discord.ext import commands


def is_bot_owner():
    def predicate(ctx):
        return ctx.message.author.id == constants.OWNER_ID
    return commands.check(predicate)


def can_manage_roles():
    def predicate(ctx):
        return ctx.author.guild_permissions.manage_roles
    return commands.check(predicate)


def can_manage_messages():
    def predicate(ctx):
        return ctx.author.guild_permissions.manage_messages
    return commands.check(predicate)


def is_guild_trusted():
    def predicate(ctx):
        trusted_role_id = database.moderation.get_trusted_role_id(ctx.guild.id)
        mod_role_id = database.moderation.get_mod_role_id(ctx.guild.id)
        admin_role_id = database.moderation.get_admin_role_id(ctx.guild.id)
        if ctx.author.guild_permissions.administrator or ctx.author.id == ctx.guild.owner_id:
            return True
        for role in ctx.guild.roles:
            if role.id == trusted_role_id or role.id == mod_role_id or role.id == admin_role_id:
                if role in ctx.author.roles:
                    return True
        return False
    return commands.check(predicate)


def is_guild_mod():
    def predicate(ctx):
        mod_role_id = database.moderation.get_mod_role_id(ctx.guild.id)
        admin_role_id = database.moderation.get_admin_role_id(ctx.guild.id)
        if ctx.author.guild_permissions.administrator or ctx.author.id == ctx.guild.owner_id:
            return True
        for role in ctx.guild.roles:
            if role.id == mod_role_id or role.id == admin_role_id:
                if role in ctx.author.roles:
                    return True
        return False
    return commands.check(predicate)


def is_guild_admin():
    def predicate(ctx):
        admin_role_id = database.moderation.get_admin_role_id(ctx.guild.id)
        if ctx.author.guild_permissions.administrator or ctx.author.id == ctx.guild.owner_id:
            return True
        for role in ctx.guild.roles:
            if role.id == admin_role_id:
                if role in ctx.author.roles:
                    return True
        return False
    return commands.check(predicate)


def is_guild_owner():
    def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id
    return commands.check(predicate)
