import os
import discord
from discord.ext import commands
import json

client = commands.Bot(command_prefix="?")
client.remove_command("help")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


with open("./config/config.json" , "r") as config:
    conf = json.load(config)
    extension_list = conf["extensions"]
    for ext in extension_list:
        client.load_extension(ext.strip())

client.run(os.environ.get("BOT_TOKEN "))
