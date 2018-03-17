import log
import asyncio
import discord
import constants
import database
from discord.ext import commands


def start(bot: commands.Bot):
    print('Adding listeners.')
    bot.add_listener(delete_messages_in_auto_delete_channels, 'on_message')
    bot.add_listener(anti_ghost, 'on_message')
    bot.add_listener(log.log_standard_action, 'on_command_completion')
    bot.add_listener(post_leave_message, 'on_member_remove')


def remove(bot: commands.Bot):
    print('Removing listeners.')
    bot.remove_listener(delete_messages_in_auto_delete_channels)
    bot.remove_listener(anti_ghost)
    bot.remove_listener(log.log_standard_action)
    bot.remove_listener(post_leave_message)


async def delete_messages_in_auto_delete_channels(message: discord.Message):
    if message.channel.id in constants.AUTO_DELETE_IDS:
        await asyncio.sleep(constants.AUTO_DELETE_AFTER)
        await message.delete()


async def anti_ghost(message: discord.Message):
    if database.moderation.get_ghosting(message.guild.id):
        return
    if message.author.status == discord.Status.offline:
        await message.delete()
        print('Deleted message from offline user')
        await message.author.send(f'👻 Ghosting is not enabled on {message.guild.name}.\n'
                                  f'Switch your status to online/afk/dnd instead of invisible.', delete_after=60)


async def post_leave_message(member: discord.Member):
    leave_message = database.moderation.get_leave_message(member.guild.id)
    leave_message = constants.DEFAULT_LEAVE_MESSAGE if not leave_message else leave_message
    leave_message = leave_message\
        .replace('{{user}}', str(member))\
        .replace('{{server}}', member.guild.name)
    channel = member.guild.get_channel(database.moderation.get_leave_channel_id(member.guild.id))
    if not channel:
        channel = member.guild.system_channel
    await channel.send(leave_message)


# Not being used at the moment
async def listen_for_stars(reaction: discord.Reaction, user: discord.Member):
    if reaction.emoji in ['🌟', '⭐'] and reaction.count > 1:
        star_channel_id = database.moderation.get_star_channel_id(reaction.message.guild.id)
        star_channel = reaction.message.guild.get_channel(star_channel_id)
        if not star_channel:
            return
        embed = discord.Embed(description=reaction.message.content)
        embed.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url)