import json
from discord.ext import commands
import discord
import os
from json import loads


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, service_name):
        data = ""
        for filename in os.listdir("./services"):
            if filename.endswith(".json"):
                if filename.lower() == service_name.lower().strip() + ".json":
                    data = filename
                    break
        if data == "":
            await ctx.send(f"Service {service_name} is not supported")
            return False
        with open(f"./services/{data}", "r") as info:
            data = loads(info.read())
        infoEmbed = discord.Embed(title=service_name, color=discord.Color.from_rgb(102, 191, 191))
        infoEmbed.set_thumbnail(url=data["image"])
        infoEmbed.add_field(name="Website", value=data["website"])
        infoEmbed.add_field(name="Calculator", value=data["calculator"])
        await ctx.send(embed=infoEmbed)


def setup(client):
    client.add_cog(Info(client))
