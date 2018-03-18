import log
import asyncio
import discord
import utility
import constants
from database import moderation, stars
from discord.ext import commands


def start(bot: commands.Bot):
    print('Adding listeners.')
    bot.add_listener(delete_messages_in_auto_delete_channels, 'on_message')
    bot.add_listener(anti_ghost, 'on_message')
    bot.add_listener(log.log_standard_action, 'on_command_completion')
    bot.add_listener(post_leave_message, 'on_member_remove')
    bot.add_listener(listen_for_stars, 'on_reaction_add')


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
    if moderation.get_ghosting(message.guild.id):
        return
    if message.author.status == discord.Status.offline:
        await message.delete()
        await message.author.send(f'👻 Ghosting is not enabled on {message.guild.name}.\n'
                                  f'Switch your status to online/afk/dnd instead of invisible.', delete_after=60)


async def post_leave_message(member: discord.Member):
    leave_message = moderation.get_leave_message(member.guild.id)
    leave_message = constants.DEFAULT_LEAVE_MESSAGE if not leave_message else leave_message
    leave_message = utility.format_string_with_member_data(leave_message, member)
    channel = member.guild.get_channel(moderation.get_leave_channel_id(member.guild.id))
    if not channel:
        channel = member.guild.system_channel
    await channel.send(leave_message)


async def listen_for_stars(reaction: discord.Reaction, member: discord.Member):
    if reaction.emoji == '🌟' and reaction.count > 1:
        star_channel = None
        for channel in member.guild.text_channels:
            if channel.name == 'starboard' or channel.name == 'stars':
                star_channel = channel
                break
        if not star_channel:
            return
        if not stars.is_starred(reaction.message):
            embed = discord.Embed(description=reaction.message.content, color=discord.Color.gold())
            embed.set_author(name=f'{reaction.message.author.name}#{reaction.message.author.discriminator}',
                             icon_url=reaction.message.author.avatar_url)
            embed.timestamp = reaction.message.created_at
            embed.set_footer(text=f'<#{reaction.message.channel.id}>')
            try:
                embed.set_image(url=reaction.message.attachments[0].url)
            except (AttributeError, IndexError):
                pass
            star = await star_channel.send(embed=embed)
            stars.add(reaction.message, star)
