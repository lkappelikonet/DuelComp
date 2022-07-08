import json
import discord
from discord.ext import commands


class Resource(commands.Cog):
    def __init__(self, _client):
        self._client = _client

        # Load the resource dictionary
        with open(r"resources\ygo_resources.json", encoding='utf8') as json_file:
            self.ygo_resources = json.load(json_file)

    @commands.group(
        name="resource",
        aliases=['r'],
        help='Useful resources for understanding YGO. "+r" for more info.'
    )
    async def resource(self, command_context, *args):
        if not args: # If no arguments were provided, show all the allowable arguments

            # List the commands as an embed
            command_list_embed = discord.Embed(color=discord.Color.blue())

            for resource_category in self.ygo_resources:
                for resource_entry in self.ygo_resources[resource_category]:
                    command_list_embed.add_field(
                        name=f"+r {self.ygo_resources[resource_category][resource_entry]['alias']} : "
                             f"{self.ygo_resources[resource_category][resource_entry]['title']}",
                        value=self.ygo_resources[resource_category][resource_entry]['help'],
                        inline=False
                    )
            await command_context.send(embed=command_list_embed)
            return

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
        else:
            await command_context.send("Conclusion: Resource not found. Perhaps you misspelled it?")
        return
