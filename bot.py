import checks
import asyncio
import discord
import requests
import listeners
from importlib import reload
from discord.ext import commands

try:
    # noinspection PyUnresolvedReferences
    import constants
except ImportError:
    print('You haven\'t renamed constants.example.py! Make sure all values are set and the file exists.')
    exit()

bot = commands.Bot(command_prefix=constants.PREFIX, owner_id=constants.OWNER_ID)
auto_loaded_extensions = [
    # 'core',  # TODO: Migrate core commands to this
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


@bot.check
def is_not_dm(ctx):
    return isinstance(ctx.channel, discord.TextChannel)


@bot.group()
@checks.is_bot_owner()
async def core(ctx):
    pass


@core.command()
async def restart(ctx):
    await ctx.message.add_reaction('🔄')
    await bot.logout()
    exit(0)


@core.command()
async def kill(ctx):
    """
    You have no idea how fucking painful it was to write this. The bot would exit with code 1, but no matter what,
    the batch file running it always had an errorlevel of 0. The only way I managed to get this working was
    by creating an empty file and then checking in the batch file whether it exists or not. If it exists, the bot
    gets killed, if it doesn't then the bot restarts. Super janky but it's literally the only way I found to do it.
    """
    await ctx.send(f'<@{ctx.author.id}> You must react to this message within 1 minute to kill me.')
    reaction, user = await bot.wait_for('reaction_add', timeout=60, check=lambda r, u: u.id == constants.OWNER_ID)
    open('kill.txt', 'w').close()
    await bot.logout()
    await asyncio.sleep(1)
    exit()


@core.command(name='reload')
async def reload_cog(ctx, cog: str):
    if cog == 'listeners':
        listeners.remove(bot)
        reload(listeners)
        listeners.start(bot)
    elif cog == '*':
        loaded_extensions = bot.extensions
        for ext in set(loaded_extensions):
            bot.unload_extension(ext)
            bot.load_extension(ext)
    else:
        try:
            bot.unload_extension(f'cogs.{cog}')
            bot.load_extension(f'cogs.{cog}')
        except (AttributeError, ImportError, discord.ClientException) as e:
            await ctx.send(f'Reloading `{cog}` failed.',
                           embed=discord.Embed(title=f'**{str(type(e))}**',
                                               description=str(e),
                                               color=discord.Color.red()))
            return
        await ctx.message.add_reaction('👍')


@core.command()
async def load(ctx, cog: str):
    try:
        bot.load_extension(f'cogs.{cog}')
    except (AttributeError, ImportError, discord.ClientException) as e:
        await ctx.send(f'Loading `{cog}` failed.',
                       embed=discord.Embed(title=f'**{str(type(e))}**',
                                           description=str(e),
                                           color=discord.Color.red()))
    else:
        await ctx.message.add_reaction('👍')


@core.command()
async def unload(ctx, cog: str):
    try:
        bot.unload_extension(f'cogs.{cog}')
    except (AttributeError, ImportError, discord.ClientException) as e:
        await ctx.send(f'Unloading `{cog}` failed.',
                       embed=discord.Embed(title=f'**{str(type(e))}**',
                                           description=str(e),
                                           color=discord.Color.red()))
    else:
        await ctx.message.add_reaction('👍')


@core.group(name='get')
async def get(ctx):
    pass


@get.command()
async def invite(ctx):
    await ctx.message.add_reaction('✉')
    await ctx.author.send(constants.INVITE_URL.replace('<ID>', str(bot.user.id)))


@get.command()
async def ip(ctx: commands.Context):
    with ctx.typing():
        bot_ip = requests.get('https://api.ipify.org/').content.decode()
        await ctx.author.send(bot_ip)
        await ctx.send(content='Host\'s public IP has been sent to your DMs.', delete_after=5)


@get.command(aliases=['cogs'])
async def extensions(ctx):
    current_ext = ''
    for ext in bot.extensions:
        current_ext += f'{ext}\n'
    await ctx.send(current_ext if current_ext else 'No cogs loaded.')

if __name__ == '__main__':
    bot.run(constants.TOKEN)
