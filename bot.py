import listeners
import discord
import utility
import log
from discord.ext import commands
import database.commands

try:
    # noinspection PyUnresolvedReferences
    import constants
except ImportError:
    print('You haven\'t renamed constants.example.py! Make sure all values are set and the file exists.')
    exit()

bot = commands.Bot(command_prefix=constants.PREFIX, owner_id=constants.OWNER_ID)
auto_loaded_extensions = [
    'core',
    'roles',
    'moderation',
    'fun',
    'commands'
]


def load_exts():
    for ext in auto_loaded_extensions:
        bot.load_extension(f'cogs.{ext}')


@bot.event
async def on_ready():
    print('Kevin Rudd bot ready.')
    print(f'Logged in as `{bot.user.name}`')
    load_exts()
    listeners.start(bot)


async def custom_command_call(message: discord.Message):
    if message.author.bot:
        return
    length_of_prefix = len(constants.PREFIX)
    if message.content[0:length_of_prefix] == constants.PREFIX:
        command_name = message.content[length_of_prefix:].strip()
        command_response = database.commands.get_command(message.guild, command_name)
        if not command_response:
            return
        await message.channel.send(utility.format_string_with_message_data(command_response, message))
        await log.log_standard_action(message)


if __name__ == '__main__':
    bot.run(constants.TOKEN)
    bot.add_listener(custom_command_call, 'on_message')
