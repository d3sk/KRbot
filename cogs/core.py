import requests

import checks
import discord
import asyncio
import constants
import listeners
from importlib import reload
from discord.ext import commands


class Core:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @checks.is_bot_owner()
    async def core(self, ctx):
        pass

    @core.command()
    async def restart(self, ctx):
        await ctx.message.add_reaction('🔄')
        await self.bot.logout()
        exit(0)

    @core.command()
    async def kill(self, ctx):
        """
        You have no idea how fucking painful it was to write this. The bot would exit with code 1, but no matter what,
        the batch file running it always had an errorlevel of 0. The only way I managed to get this working was
        by creating an empty file and then checking in the batch file whether it exists or not. If it exists, the bot
        gets killed, if it doesn't then the bot restarts. Super janky but it's literally the only way I found to do it.
        """
        await ctx.send(f'<@{ctx.author.id}> You must react to this message within 1 minute to kill me.')
        reaction, user = await self.bot.wait_for('reaction_add',
                                                 timeout=60,
                                                 check=lambda r, u: u.id == constants.OWNER_ID)
        open('kill.txt', 'w').close()
        await self.bot.logout()
        await asyncio.sleep(1)
        exit()

    @core.command(name='reload')
    async def reload_cog(self, ctx, cog: str):
        if cog == 'listeners':
            listeners.remove(self.bot)
            reload(listeners)
            listeners.start(self.bot)
        elif cog == '*':
            loaded_extensions = self.bot.extensions
            for ext in set(loaded_extensions):
                self.bot.unload_extension(ext)
                self.bot.load_extension(ext)
        else:
            try:
                self.bot.unload_extension(f'cogs.{cog}')
                self.bot.load_extension(f'cogs.{cog}')
            except (AttributeError, ImportError, discord.ClientException) as e:
                await ctx.send(f'Reloading `{cog}` failed.',
                               embed=discord.Embed(title=f'**{str(type(e))}**',
                                                   description=str(e),
                                                   color=discord.Color.red()))
                return
        await ctx.message.add_reaction('👍')

    @core.command()
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(f'cogs.{cog}')
        except (AttributeError, ImportError, discord.ClientException) as e:
            await ctx.send(f'Loading `{cog}` failed.',
                           embed=discord.Embed(title=f'**{str(type(e))}**',
                                               description=str(e),
                                               color=discord.Color.red()))
        else:
            await ctx.message.add_reaction('👍')

    @core.command()
    async def unload(self, ctx, cog: str):
        try:
            if cog != 'core':
                self.bot.unload_extension(f'cogs.{cog}')
            else:
                await ctx.send('Cannot unload core.')
                return
        except (AttributeError, ImportError, discord.ClientException) as e:
            await ctx.send(f'Unloading `{cog}` failed.',
                           embed=discord.Embed(title=f'**{str(type(e))}**',
                                               description=str(e),
                                               color=discord.Color.red()))
        else:
            await ctx.message.add_reaction('👍')

    @core.group(name='get')
    async def get(self, ctx):
        pass

    @get.command()
    async def invite(self, ctx):
        await ctx.message.add_reaction('✉')
        await ctx.author.send(constants.INVITE_URL.replace('<ID>', str(self.bot.user.id)))

    @get.command()
    async def ip(self, ctx: commands.Context):
        with ctx.typing():
            bot_ip = requests.get('https://api.ipify.org/').content.decode()
            await ctx.author.send(bot_ip)
            await ctx.send(content='Host\'s public IP has been sent to your DMs.', delete_after=5)

    @get.command(aliases=['cogs'])
    async def extensions(self, ctx):
        current_ext = ''
        for ext in self.bot.extensions:
            current_ext += f'{ext}\n'
        await ctx.send(current_ext if current_ext else 'No cogs loaded.')


def setup(bot):
    bot.add_cog(Core(bot))
    print(f'Extension "{__name__}" has been added.')


def teardown(bot):
    print(f'Extension "{__name__}" has been removed.')
