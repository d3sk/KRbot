import discord
import checks
import constants
import database.moderation
from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help='Provides access to information about the server, stored by the bot. '
                         f'`{constants.PREFIX}help server` for more information.',
                    aliases=['guild'])
    @checks.is_guild_mod()
    async def server(self, ctx):
        pass

    @server.group(help=f'Set a value in the database. `{constants.PREFIX}help server set` for more information.')
    async def set(self, ctx):
        pass

    @set.group(name='message')
    async def message_group(self, ctx):
        pass

    @message_group.command(name='leave')
    @checks.is_guild_mod()
    async def set_leave_message(self, ctx, *, leave_message: str):
        database.moderation.set_leave_message(ctx.guild, leave_message)
        await ctx.send(f'The new leave message is: {database.moderation.get_leave_message(ctx.guild.id)}')

    @set.group(name='channel')
    async def channel_group(self, ctx):
        pass

    @channel_group.command(name='leave')
    @checks.is_guild_mod()
    async def set_leave_channel(self, ctx, *, channel: discord.TextChannel):
        database.moderation.set_leave_channel_id(channel)
        await ctx.send(f'The new leave announcement channel is '
                       f'<#{database.moderation.get_leave_channel_id(ctx.guild.id)}>.')

    # /server set channel logs #get-roles
    @channel_group.command(name='logs')
    @checks.is_guild_admin()
    async def set_logs_channel(self, ctx, *, channel: discord.TextChannel):
        database.moderation.set_log_channel_id(channel)
        await ctx.send(f'The new log channel is <#{database.moderation.get_log_channel_id(ctx.guild.id)}>.')

    @set.group(name='role')
    async def role_group(self, ctx):
        pass

    @set.command(name='ghosting')
    async def set_ghosting(self, ctx, value: bool):
        database.moderation.set_ghosting(value, ctx.guild.id)
        await ctx.send('Ghosting is now ' +
                       ('enabled.' if database.moderation.get_ghosting(ctx.guild.id) else 'disabled.'))

    # /server set role admin Shadow Cabinet
    @role_group.command(name='admin', aliases=['admins'])
    @checks.is_guild_owner()
    async def set_admin_in_db(self, ctx, *, role: discord.Role):
        database.moderation.set_admin_role_id(role)
        await ctx.send(f'The new admin role is <@&{database.moderation.get_admin_role_id(ctx.guild.id)}>.')

    # /server set role trusted Young Labor
    @role_group.command(name='trusted')
    @checks.is_guild_admin()
    async def set_trusted_in_db(self, ctx, *, role: discord.Role):
        database.moderation.set_trusted_role_id(role)
        await ctx.send(f'The new trusted role is <@&{database.moderation.get_trusted_role_id(ctx.guild.id)}>.')

    # /server set role mod Labor Party
    @role_group.command(name='mod', aliases=['mods'])
    @checks.is_guild_admin()
    async def set_mod_in_db(self, ctx, *, role: discord.Role):
        database.moderation.set_mod_role_id(role)
        await ctx.send(f'The new moderator role is <@&{database.moderation.get_mod_role_id(ctx.guild.id)}>.')

    # /server set role mute Muted
    @role_group.command(name='mute', aliases=['muted'])
    @checks.is_guild_mod()
    async def set_mute_in_db(self, ctx, *, role: discord.Role):
        if role > ctx.guild.me.top_role:
            await ctx.send(f'{role.name} is above my top role, I won\'t be able to mute users. '
                           f'Move the role and try again.')
            return
        database.moderation.set_mute_role_id(role)
        await ctx.send(f'The new mute role is <@&{database.moderation.get_mute_role_id(ctx.guild.id)}>.')

    @commands.command()
    @checks.is_guild_mod()
    async def mute(self, ctx, member: discord.Member):
        mute_role_id = database.moderation.get_mute_role_id(ctx.guild.id)
        if member.id == ctx.author.id:
            await ctx.send('You can\'t mute yourself.')
            return
        if not mute_role_id:
            await ctx.send('This server doesn\'t have a mute role set.\n'
                           'Ask the server owner to use `/server set role mute <role name>` to set one.')
            return
        for role in ctx.guild.roles:
            if role.id == mute_role_id:
                if role > ctx.guild.me.top_role:
                    await ctx.send(f'{role.name} is higher than my top role, I can\'t assign that.')
                    return
                if role in member.roles:
                    await member.remove_roles(role)
                    await ctx.send(f'`{member.name}` has now been un-muted.')
                else:
                    await member.add_roles(role)
                    await ctx.send(f'`{member.name}` has now been muted.')
                return
        await ctx.send('The server has a mute role set, but it wasn\'t in the roles.'
                       'Ask an admin to use `/server set role mute <role name>` to update it.')

    @commands.command()
    @checks.is_guild_mod()
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send('I don\'t have permission to kick users!')
            return
        if member == ctx.guild.me:
            await ctx.send('I can\'t kick myself.')
            return
        elif member.id == ctx.author.id:
            await ctx.send('You can\'t kick yourself.')
            return
        elif member.top_role == ctx.guild.me.top_role:
            await ctx.send(f'I can\'t kick {member.name}, we share the same highest role.')
            return
        elif member.top_role > ctx.guild.me.top_role:
            await ctx.send(f'{member.name} has a higher role than me, I can\'t kick them.')
            return
        else:
            try:
                await ctx.guild.kick(member, reason=reason)
            except discord.Forbidden as e:
                await ctx.send(f'Something went wrong trying to kick {member.name}.',
                               embed=discord.Embed(title=f'**{str(type(e))}**',
                                                   description=str(e),
                                                   color=discord.Color.red()))
            else:
                await ctx.message.add_reaction('👍')

    @commands.command()
    @checks.is_guild_mod()
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.send('I don\'t have permission to ban users!')
            return
        if member == ctx.guild.me:
            await ctx.send('I can\'t ban myself.')
            return
        elif member.id == ctx.author.id:
            await ctx.send('You can\'t ban yourself.')
            return
        elif member.top_role == ctx.guild.me.top_role:
            await ctx.send(f'I can\'t ban {member.name}, we share the same highest role.')
            return
        elif member.top_role > ctx.guild.me.top_role:
            await ctx.send(f'{member.name} has a higher role than me, I can\'t ban them.')
            return
        else:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.Forbidden as e:
                await ctx.send(f'Something went wrong trying to ban {member.name}.',
                               embed=discord.Embed(title=f'**{str(type(e))}**',
                                                   description=str(e),
                                                   color=discord.Color.red()))
            else:
                await ctx.message.add_reaction('🔨')

    @commands.command(name='purge', aliases=['prune'])
    @checks.is_guild_trusted()
    async def _purge(self, ctx, amount: int):
        if amount > 200:
            await ctx.send(f'{amount} is too many messages! Limit is 200.')
        else:
            await ctx.message.channel.purge(limit=amount + 1)


def setup(bot):
    bot.add_cog(Moderation(bot))
    print(f'Extension "{__name__}" has been added.')


def teardown(bot):
    print(f'Extension "{__name__}" has been removed.')
