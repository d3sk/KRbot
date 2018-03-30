import constants
import log
import discord
from discord.ext import commands


class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='echo')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def echo_input(self, ctx, *, message: str):
        if len(message) < 300:
            await ctx.send(message)
            await ctx.message.delete()
        else:
            await ctx.send(f'Echoes must be under 300 characters, that was {len(message)}.')

    @commands.command(name='quote', enabled=False, hidden=True)
    async def quote_message(self, ctx, message_id: int):
        pass


def setup(bot):
    bot.add_cog(Fun(bot))
    # bot.add_listener(Moderation.listen_for_stars, 'on_reaction_add')
    print(f'Extension "{__name__}" has been added.')


def teardown(bot):
    print(f'Extension "{__name__}" has been removed.')
