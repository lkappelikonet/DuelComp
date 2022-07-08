import json

import discord
from discord.ext import commands


class Configuration(commands.Cog):
    """Handles settings like where the bot can post what.
    _client is the bot\'s client
    guild_configs is a dictionary, loaded/saved from guild_configs.json, which keep track of the config settings"""

    def __init__(self, _client):
        self._client = _client

        # Load the guild configurations from the json file
        with open(r"resources\guild_configs.json", encoding='utf8') as json_file:
            self.guild_configs = json.load(json_file)

        #TODO upon being added to a guild, add a new config file

        return

    def __del__(self):  # Once done with the cog, write the guild configurations to the json file.
        for guild in self._client.guilds: self.initialize_guild_config(guild) # covering bases.
        with open(r"resources\guild_configs.json", 'w', encoding='utf8') as json_file:
            json.dump(self.guild_configs, json_file)
        return

    def initialize_guild_config(self, guild): # called when a new config entry is needed for a new guild
        if str(guild.id) not in [*self.guild_configs.keys()]:
            self.guild_configs[guild.id] = {
                'bot_channel': -1,
                'resource_channel': []
            }
        return

    async def bot_log(self, context, message):
        bot_channel = context.guild.get_channel(int(self.guild_configs[str(context.guild.id)]['bot_channel']))
        if bot_channel != -1:
            if isinstance(message, str):
                await bot_channel.send(message)
            elif isinstance(message, discord.Embed):
                await bot_channel.send(embed=message)
        await context.message.delete()
        return

    @commands.group(
        name='config',
        aliases=['c'],
        help='Bot configuration tools.',
        invoke_without_command=True
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def config(self, command_context):
        help_embed = discord.Embed(
            title='[+c | +config] : Configuration Commands',
            description='List the commands available within the configuration cog.',
            color=discord.colour.Color.blue()
        )
        help_embed.add_field(
            name='+c [set | s]',
            value='Sets a configuration setting for this guild.'
        )
        help_embed.add_field(
            name='+c [get | g]',
            value='Gets a configuration setting for this guild.'
        )
        await self.bot_log(command_context, help_embed)
        return

    @config.command(
        name='set',
        aliases=['s'],
        help='Set a configuration setting for this guild.'
    )
    async def set(self, command_context, *args):

        # If no parameters are provided, show what parameters are available to set
        if len(args) == 0:
            help_embed = discord.Embed(
                title='+c [set | s] <parameter> <value?>: Set Guild Configuration',
                description='Set a setting for this guild\'s configuration',
                color=discord.colour.Color.blue()
            )
            help_embed.add_field(
                name='bot_channel',
                value='Toggles this channel as the target for meta-information messages from the bot.',
            )
            help_embed.add_field(
                name='resource_channel',
                value='Toggles this channel as able to use resource [+r] commands. Call again to remove from the list.',
            )
            await self.bot_log(command_context, help_embed)
            return

        # Check to see if the configuration is allowable.
        if args[0] not in [*self.guild_configs[str(command_context.guild.id)].keys()]:
            await self.bot_log(command_context, f"Statement: ```{args[0]}``` is not a valid configuration parameter.")
        elif args[0] == 'bot_channel':
            if self.guild_configs[str(command_context.guild.id)][args[0]] == command_context.channel.id:
                self.guild_configs[str(command_context.guild.id)][args[0]] = -1
                await self.bot_log(command_context, f'{command_context.channel.name} rescinded as the bot channel.')
            else:
                self.guild_configs[str(command_context.guild.id)][args[0]] = command_context.channel.id
                await self.bot_log(command_context, f'{command_context.channel.name} set as the bot channel.')

        elif args[0] == 'resource_channel':
            if command_context.channel.id in self.guild_configs[str(command_context.guild.id)][args[0]]:
                del self.guild_configs[str(command_context.guild.id)][args[0]][command_context.channel.id]
                await self.bot_log(command_context, f'{command_context.channel.name} removed from resource_channels')
            else:
                self.guild_configs[str(command_context.guild.id)][args[0]].append(command_context.channel.id)
                await self.bot_log(command_context, f'{command_context.channel.name} added to resource_channels')
        return

    @config.command(
        name='get',
        aliases=['g'],
        help='Get a configuration setting for this guild.'
    )
    async def getconfig(self, command_context, *args):
        if len(args) == 0: # If no arguments are passed, print the full configuration
            help_embed = discord.Embed(
                title='+c [get : g] <parameter>',
                description='List the guild configuration for <parameter>',
                color=discord.colour.Color.blue()
            )
            for key in [*self.guild_configs[str(command_context.guild.id)].keys()]:
                if isinstance(self.guild_configs[str(command_context.guild.id)][key], list):
                    help_embed.add_field(
                        name=key,
                        value='\n'.join([
                            command_context.guild.get_channel(channel_id).name for channel_id in self.guild_configs[str(command_context.guild.id)][key]
                        ])
                    )
                else:
                    help_embed.add_field(
                        name=key,
                        value= command_context.guild.get_channel(self.guild_configs[str(command_context.guild.id)][key]).name
                    )

            await self.bot_log(command_context, help_embed)
        else:
            if args[0] not in [*self.guild_configs[str(command_context.guild.id)].keys()]:
                await self.bot_log(command_context, f"Statement: ```{args[0]}``` is an invalid configuration parameter.")
            else:
                description = ''
                if isinstance(self.guild_configs[str(command_context.guild.id)][args[0]], list):
                    description = '\n'.join([
                        command_context.guild.get_channel(channel_id).name for channel_id in self.guild_configs[str(command_context.guild.id)][args[0]]
                    ])
                else:
                    description = command_context.guild.get_channel(self.guild_configs[str(command_context.guild.id)][args[0]]).name
                await self.bot_log(command_context, discord.Embed(
                    title=args[0],
                    description=description,
                    color=discord.colour.Color.blue()
                ))

        return

# channels: resource, bot, welcome,
