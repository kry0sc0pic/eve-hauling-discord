import discord
from discord import embeds
from discord.ext import commands
from requests import request
from json import loads

payload = {}
headers = {
    "User-Agent": "EVE Hauling Discord Bot"}


class BlackFrog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def blackfrog(self, ctx, origin, destination, collateral, volume):
        URL = f"https://red-frog.org/api/public/v1/calculator/black/?origin={origin}&destination={destination}&collateral={collateral}"
        response = request("GET", URL, headers=headers, data=payload)
        data = loads(response.content.decode("utf-8"))
        if data.get("error"):
            msg = data["error"]
            await ctx.send(f"**Error:** *{msg}*")
        elif ((maxVolume := data["volume"]) <= int(volume)):
            await ctx.send(f"**Error:** *Volume Above limit {maxVolume}*")
        else:
            contractEmbed = discord.Embed(title="Black frog Freight",
                                          description="Details for your courier contract with Black Frog Freight",
                                          color=discord.Color.from_rgb(34, 40, 49)
                                          )
            contractEmbed.set_thumbnail(url="https://red-frog.org/img/rf_alliance.png")
            contractEmbed.add_field(name="Origin System", value=data["origin_name"])
            contractEmbed.add_field(name="Destination System", value=data["destination_name"])
            contractEmbed.add_field(name="Collateral", value=str(data["collateral"]) + " ISK")
            contractEmbed.add_field(name="Reward", value=str(data["reward_base"]) + " ISK")
            contractEmbed.add_field(name="Days To Complete", value=str(data["days_to_complete"]) + " Days")
            contractEmbed.add_field(name="Days To Accept", value=str(data["days_expiration"]) + " Days")
            contractEmbed.add_field(name="Corporation", value=data["corporation"])
            contractEmbed.set_footer(
                text="If you are adding containers in the contract , mention containers in the description and consider a tip!")
            await ctx.send(embed=contractEmbed)


def setup(client):
    client.add_cog(BlackFrog(client))
