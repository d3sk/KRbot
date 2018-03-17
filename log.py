import constants
import database.moderation
import discord
from datetime import datetime
from pytz import timezone


async def log_standard_action(ctx):
    try:
        if ctx.command.root_parent.name == 'core':
            return
    except AttributeError:
        pass

    log_channel = ctx.guild.get_channel(database.moderation.get_log_channel_id(ctx.guild.id))
    if not log_channel:
        return
    embed = discord.Embed(color=discord.Color.blurple())
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    embed.timestamp = datetime.now(timezone(constants.HOST_TIMEZONE))
    embed.title = 'Command'
    try:
        embed.description = ctx.message.content
    except AttributeError:
        embed.description = ctx.content
    embed.add_field(name='Channel', value=f'<#{ctx.channel.id}>')
    embed.set_footer(text=f'User ID: {ctx.author.id}')
    await log_channel.send(embed=embed)


async def log_user_kick_or_ban(ctx):
    pass
