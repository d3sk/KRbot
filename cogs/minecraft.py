import json
import checks
import requests
from discord.ext import commands


class MinecraftServerManagement:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @checks.is_bot_owner()
    async def minecraft(self, ctx):
        pass

    @minecraft.group(name='server')
    @checks.is_bot_owner()
    async def server_management(self, ctx):
        pass

    @server_management.command()
    async def status(self, ctx):
        await ctx.trigger_typing()
        r = requests.get('https://mcapi.us/server/status?ip=' +
                         requests.get('https://api.ipify.org').content.decode().strip())
        j = json.loads(r.content.decode())
        status = j.get('online')
        await ctx.send('Server is currently ' + ('online.' if status else 'offline.'))

    @server_management.command()
    async def ip(self, ctx):
        await ctx.trigger_typing()
        ip = requests.get('https://api.ipify.org').content.decode().strip()
        await ctx.send(f'Current host IP is `{ip}`')


def setup(bot):
    bot.add_cog(MinecraftServerManagement(bot))
    print(f'Extension "{__name__}" has been added.')


def teardown(bot):
    print(f'Extension "{__name__}" has been removed.')
