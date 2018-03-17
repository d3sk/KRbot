import listeners
from discord.ext import commands

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
    'commands',
    'minecraft'
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


if __name__ == '__main__':
    bot.run(constants.TOKEN)
