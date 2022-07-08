import os
import re

import discord
from discord.ext import commands
from dotenv import load_dotenv

import api_handler
import cog_moderation
import cog_resource

load_dotenv()
_client = commands.Bot(
    command_prefix='+',
    activity=discord.Game(name='+help')
)


@_client.event
async def on_ready(): print(f'System {_client.user} initialized. Beginning guild observation.')


@_client.command(name='testing')
@commands.is_owner()
async def testing(ctx):
    api_handler.dbpoke()
    await ctx.send("System check is complete; no problems found.")


@_client.event
async def on_message(message):
    if message.author == _client.user:
        return

    # Greeting
    if re.compile(r"^(good (morning|day|afternoon|evening)|greetings|hello).{1,2}duel.?(bot|machine|comp)",
                  re.IGNORECASE).match(message.content):
        await message.channel.send(f'Greetings, {message.author.display_name}.')

    # Insult handling
    if re.compile(r".*suck.*duel.?(bot|mach|comp)",
                  re.IGNORECASE).match(message.content):
        await message.channel.send(f'An amusing attempt to hurt my algorithmic feelings, meatbag.')

    await _client.process_commands(message)


@_client.event
async def on_error(event, *args):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


_client.add_cog(cog_resource.Resource(_client))
_client.add_cog(cog_moderation.Configuration(_client))
_client.run(os.getenv('TOKEN'))
