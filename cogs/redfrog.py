import discord
from discord.ext import commands
from requests import request
from json import loads

payload = {}
headers = {
    "User-Agent": "EVE Hauling Discord Bot"}


class RedFrog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def redfrog(self, ctx, origin, destination, collateral, volume):
        URL = f"https://red-frog.org/api/public/v1/calculator/red/?origin={origin}&destination={destination}"
        response = request("GET", URL, headers=headers, data=payload)
        data = loads(response.content.decode("utf-8"))
        maxVolume = data["volume"]
        maxCollat = data["collateral"]
        if data.get("error"):
            msg = data["error"]
            await ctx.send(f"**Error:** *{msg}*")
        elif (maxVolume <= int(volume)):
            await ctx.send(f"**Error:** *Volume Above limit {maxVolume} m3*")
        elif (maxCollat <= int(collateral)):
            await ctx.send(f"**Error:** *Collateral Above limit {maxCollat} ISK*")
        else:
            contractEmbed = discord.Embed(title="Red Frog Freight",
                                          description="Details for your courier contract with Red Frog Freight",
                                          color=discord.Color.from_rgb(221, 44, 0)
                                          )
            contractEmbed.set_thumbnail(url="https://red-frog.org/img/rf_alliance.png")
            contractEmbed.add_field(name="Origin System", value=data["origin_name"])
            contractEmbed.add_field(name="Destination System", value=data["destination_name"])
            contractEmbed.add_field(name="Collateral", value=str(collateral) + " ISK")
            contractEmbed.add_field(name="Reward", value=str(data["reward_base"]) + " ISK")
            contractEmbed.add_field(name="Rush", value=str(data["reward_rush"]) + " ISK")
            contractEmbed.add_field(name="Days To Complete", value=str(data["days_to_complete"]) + " Days")
            contractEmbed.add_field(name="Days To Accept", value=str(data["days_expiration"]) + " Days")
            contractEmbed.add_field(name="Corporation", value=data["corporation"])
            contractEmbed.set_footer(
                text="If you are adding containers in the contract , mention containers in the description and consider a tip!")
            await ctx.send(embed=contractEmbed)


def setup(client):
    client.add_cog(RedFrog(client))
