import os
import re
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

import cog_moderation
import cog_resource


def write_debug_log(debug_text='', filepath=''):
    timestamp = datetime.now()
    if filepath == '':
        filepath = timestamp.strftime('%Y%m%d%H%M%S_Debug.txt')
    with open(filepath, 'w+', encoding='utf-8') as debugFile:
        debugFile.write(f'{timestamp.strftime("%Y.%m.%d")}\n{timestamp.strftime("%H:%M:%S")}\n\n{debug_text}')
    return


def run_bot():
    load_dotenv() # Load the environment file, which contains the bot token
    _client = commands.Bot(
        command_prefix='+',
        activity=discord.Game(name='+help')
    )

    @_client.event # Performs this when the _client triggers the on_ready event, and can perform normal activity.
    async def on_ready(): print(f'System {_client.user} initialized. Beginning guild observation.')

    @_client.command(name='testing') # Debug, +testing from discord calls this.
    @commands.is_owner() # Only run if it's me!
    async def testing(ctx):
        await ctx.send("System check is complete; no problems found.")

    @_client.event # handle messages before passing them to the command processing. Just greetings and insult handling
    async def on_message(message):
        if message.author == _client.user: return # Don't respond to yourself, bot!

        # Greeting
        if re.compile(r"^(good (morning|day|afternoon|evening)|greetings|hello).{1,2}duel.?(bot|machine|comp)",
                      re.IGNORECASE).match(message.content):
            await message.channel.send(f'Greetings, {message.author.display_name}.')

        # Insult handling
        if re.compile(r".*suck.*duel.?(bot|mach|comp)",
                      re.IGNORECASE).match(message.content):
            await message.channel.send(f'An amusing attempt to hurt my algorithmic feelings, meatbag.')

        await _client.process_commands(message) # after conversations, pass the message to the command handler

    @_client.event # When an error happens, write it to the console
    async def on_error(event, *args):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise

    # Attach the cogs to the _client. This gives it the commands and how to process them.
    _client.add_cog(cog_resource.Resource(_client))
    _client.add_cog(cog_moderation.Configuration(_client))
    _client.run(os.getenv('TOKEN')) # Run the client!


run_bot()
