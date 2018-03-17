import constants
import database.roles
import re
import checks
import discord
from discord.ext import commands


def sanitize_args(match_object):
    return match_object.group(1), match_object.group(2)


def member_has_role(member: discord.Member, role: discord.Role):
    return True if role in member.roles else False


class Roles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Adds a role to the list of assignable roles. Must be quoted if it has a space.')
    @checks.is_guild_trusted()
    async def addrole(self, ctx, role: discord.Role, alias=None):
        if role < ctx.guild.me.top_role:
            database.roles.add_role(role, alias)
            await ctx.message.add_reaction('👍')
        else:
            await ctx.send(f'`{role.name}` is above my top role. Reorganise the roles and try again.')

    @commands.command(help='DMs you a list of the guild\'s assignable roles.')
    async def roles(self, ctx):
        roles = database.roles.get_all_guild_roles(ctx.guild.id)
        pages = commands.Paginator()
        pages.add_line(f'{ctx.guild.name} has the following roles:\n')
        pages.add_line('/role <role name>    | Role assigned')
        pages.add_line('---------------------|--------------------------')
        for role in ctx.guild.role_hierarchy:
            for row in roles:
                if role.id == row.role_id:
                    pages.add_line(f'{row.alias.ljust(20)} | {role.name}')
        for page in pages.pages:
            await ctx.author.send(page)
        await ctx.message.add_reaction('✉')

    @commands.command(help='Assigns or removes a role from yourself.')
    async def role(self, ctx, *, role_name: str):
        desired_role_id = database.roles.get_from_alias(role_name, ctx.guild.id)
        if not desired_role_id:
            return
        for role in ctx.guild.roles:
            if role.id == desired_role_id:
                if member_has_role(ctx.author, role):
                    try:
                        await ctx.author.remove_roles(role)
                    except discord.Forbidden:
                        await ctx.message.channel.send(
                            f'`{role.name}` is above my top role, I can\'t remove that from users. '
                            f'Ask a moderator to fix this.')
                    else:
                        await ctx.message.add_reaction(u"\U0001F5D1")
                else:
                    try:
                        await ctx.author.add_roles(role)
                    except discord.Forbidden:
                        await ctx.message.channel.send(
                            f'`{role.name}` is above my top role, I can\'t assign that to users. '
                            f'Ask a moderator to fix this.')
                    else:
                        await ctx.message.add_reaction('👍')
                return
        database.roles.remove_role(desired_role_id)
        await ctx.send(embed=discord.Embed(
            color=discord.Color.red(),
            title='Error assigning role:',
            description=f'`{role_name}` was found in the database but not in the server roles. It\'s been deleted.'))


def setup(bot):
    bot.add_cog(Roles(bot))
    print(f'Extension "{__name__}" has been added.')


def teardown(bot):
    print(f'Extension "{__name__}" has been removed.')
