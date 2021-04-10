import discord
from discord.ext import commands, tasks
import random
import os
from itertools import cycle
from cogs import LevelSys

client = commands.Bot(command_prefix='.', intents = discord.Intents.all())
status = cycle(["Doing Road", "Out with Bro", "On the Block", "Ten Toes", "Out Ere", "Drilling"])



# Load cogs

@client.event
async def on_ready():
    change_status.start()

    cogs = [LevelSys]
    for cog in cogs:
        cog.setup(client)
        
    print('Bot is ready.')

# background task
@tasks.loop(seconds=2)
async def change_status():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))



@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')



@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt."]

    await ctx.send(f'Question: {question} \nAnswer: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter a number of messages to delete.')

client.run('ODI3ODQ5Mzk1ODE4NTk0MzE1.YGhA1A.FfUxiIXwmRAHoF0xTvzGtPReR5U')
