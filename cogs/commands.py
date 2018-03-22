import asyncio
import database.commands
import database.moderation
from discord.ext import commands
import discord
import constants
import utility
import checks
import log


class CustomCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='commands',
                    brief='Add/delete commands.',
                    help=f'Add/delete commands. List commands with {constants.PREFIX}commands')
    async def _command(self, ctx):
        if not ctx.invoked_subcommand:
            command_names = database.commands.get_all_guild_command_names(ctx.guild)
            if not command_names:
                await ctx.send('No commands found for this server!')
                return
            pages = commands.Paginator()
            pages.add_line(f'{ctx.guild} has the following custom commands:\n')
            for name in command_names:
                pages.add_line(constants.PREFIX + name)
            for page in pages.pages:
                await ctx.send(page)

    @_command.command()
    @checks.is_guild_trusted()
    async def add(self, ctx, name: str, *, response: str):
        if len(response) > 500:
            await ctx.send(f'Command responses must be under 500 characters, out of respect to other users. '
                           f'That was {len(response)} characters.')
            return
        if database.commands.get_command(ctx.guild, name):
            database.commands.delete_command(ctx.guild, name)
        database.commands.add_command(ctx.author, name, response)
        await ctx.message.add_reaction('👍')

    @_command.command(aliases=['remove'])
    @checks.is_guild_trusted()
    async def delete(self, ctx, name: str):
        if database.commands.get_command(ctx.guild, name) is None:
            await ctx.send(f'`{name}` isn\'t a command in this server.')
            return
        database.commands.delete_command(ctx.guild, name)
        await ctx.message.add_reaction('👍')

    @_command.command()
    @checks.is_guild_trusted()
    async def raw(self, ctx, name: str):
        cmd_result = database.commands.get_command(ctx.guild, name)
        if cmd_result:
            # Escape formatting characters
            await ctx.send(cmd_result.replace('\\', '\\\\').replace('`', '\`').replace('<', '\<').replace('>', '\>').replace('*', '\*').replace('_', '\_'))

    @staticmethod
    async def custom_command_call(message: discord.Message):
        """
        This static method is used as an event listener for on_message.
        It remains in this class as it only makes sense to have it here.
        """
        length_of_prefix = len(constants.PREFIX)
        if message.content[0:length_of_prefix] == constants.PREFIX:
            command_name = message.content[length_of_prefix:].strip()
            command_response = database.commands.get_command(message.guild, command_name)
            if not command_response:
                return
            await message.channel.send(utility.format_string_with_message_data(command_response, message))
            await log.log_standard_action(message)
            await asyncio.sleep(3)
            await message.delete()


def setup(bot):
    bot.add_cog(CustomCommands(bot))
    bot.add_listener(CustomCommands.custom_command_call, 'on_message')
    print(f'Extension "{__name__}" has been added.')


def teardown(bot):
    bot.remove_listener(CustomCommands.custom_command_call)
    print(f'Extension "{__name__}" has been removed.')
