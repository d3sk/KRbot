import constants
import log
import discord
import random
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

    @commands.command()
    async def choose(self, ctx, *, msg: str):
        choices = msg.split('|')
        if len(choices) > 1:
            result = random.choice(choices)
            await ctx.send(f'🎲 {result.strip()}')
        else:
            await ctx.send(f'Separate your choices with a `|` character.\n'
                           f'Example: `{constants.PREFIX}choose Tatsumaki | Kevin Rudd`')


def setup(bot):
    bot.add_cog(Fun(bot))
    # bot.add_listener(Moderation.listen_for_stars, 'on_reaction_add')
    print(f'Extension "{__name__}" has been added.')


def teardown(bot):
    print(f'Extension "{__name__}" has been removed.')
