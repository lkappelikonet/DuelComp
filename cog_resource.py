import json
import discord
from discord.ext import commands


class Resource(commands.Cog):
    """Resource cog handles commands involving writeups, links, and image resources """

    def __init__(self, _client):
        """_client is the discord.ext.commands.Bot object which acts as the interface to discord for the bot."""
        self._client = _client

        # Load the resource dictionary into memory
        with open(r"resources\ygo_resources.json", encoding='utf8') as json_file:
            self.ygo_resources = json.load(json_file)

    # Define the resource command group to allow moderation of where its commands can be used.
    @commands.group(
        name="resource",
        aliases=['r'],
        help='Useful resources for understanding YGO. "+r" for more info.'
    )
    async def resource(self, command_context, *args):
        """Resources are divided into three groups, each of which has their own way to display:
        writeups (ex. Special Summon Monsters, Damage Step Activation Legality)
        links (ex. Rulebook, Tournament Policies)
        images (ex. Fast Effect Timing Chart)"""

        if not args: # If no arguments were provided, show all the allowable arguments. Should probably be a subcommand.

            # List the commands as an embed. Blue because it looks nice.
            command_list_embed = discord.Embed(color=discord.Color.blue())

            # Iterate through the resources available by category first, and add an embed for each entry in them.
            for resource_category in self.ygo_resources:
                for resource_entry in self.ygo_resources[resource_category]:
                    command_list_embed.add_field(
                        name=f"+r {self.ygo_resources[resource_category][resource_entry]['alias']} : "
                             f"{self.ygo_resources[resource_category][resource_entry]['title']}",
                        value=self.ygo_resources[resource_category][resource_entry]['help'],
                    )
            await command_context.send(embed=command_list_embed)
            return # if no commands were added we can stop here.

        # If an argument was provided, display it, depending on what kind it is.
        if args[0] in self.ygo_resources['links']: # Links get an embed
            await command_context.send(embed=discord.Embed(
                    title=self.ygo_resources['links'][args[0]]['title'],
                    description=self.ygo_resources['links'][args[0]]['help'],
                    url=self.ygo_resources['links'][args[0]]['content']
            ))
        elif args[0] in self.ygo_resources['writeups']: # writeups are full text
            await command_context.send(
                f"__**{self.ygo_resources['writeups'][args[0]]['title']}**__\n" +
                f"{self.ygo_resources['writeups'][args[0]]['content']}"
            )
        elif args[0] in self.ygo_resources['images']: # images send their image file.
            with open(self.ygo_resources['images'][args[0]]['content'], 'rb') as image_resource:
                await command_context.send(file=discord.File(image_resource))
        else: # If the argument was not found in the dictionary, then say so.
            await command_context.send("Conclusion: Resource not found. Perhaps you misspelled it?")
        return
