from discord.ext import commands
import discord
from requests import request
from json import loads

payload = {}
headers = {}


class PushX(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pushx(self, ctx, origin, destination, collateral, volume):
        URL = f"https://api.pushx.net//api/quote/JSON/?startSystemName={origin}&endSystemName={destination}&volume={volume}&collateral={collateral}&apiClient=EVE Hauling Discord Bot"
        response = request("GET", URL, headers=headers, data=payload)
        bad_respone = False
        if response.content.decode("utf-8").lower() == "bad server response":
            await ctx.send("Maximum volume for highsec service is 1,126,500 m³")
            return False
        data = loads(response.content.decode("utf-8"))

        if data["PriceError"] != None:
            await ctx.send(data["PriceError"])
        else:
            contractEmbed = discord.Embed(title="PushX Services",
                                          description="Details for your courier contract with PushX Freight",
                                          color=discord.Color.from_rgb(0, 119, 239))
            contractEmbed.set_footer(text=data["ContainerPolicy"])
            contractEmbed.set_thumbnail(url="https://www.pushx.net/images/pushx_445.png")
            contractEmbed.add_field(name="Origin System", value=data["StartSystemName"])
            contractEmbed.add_field(name="Destination System", value=data["EndSystemName"])
            contractEmbed.add_field(name="Regular Price", value=str(data["PriceNormal"]) + " ISK")
            contractEmbed.add_field(name="Rush Price", value=str(data["PriceRush"]) + " ISK")
            contractEmbed.add_field(name="Collateral", value=str(data["Collateral"]) + " ISK")
            contractEmbed.add_field(name="Days To Accept", value=data["DaysToAccept"])
            contractEmbed.add_field(name="Days To Complete", value=data["DaysToComplete"])
            contractEmbed.add_field(name="Corporation", value=data["IssueToCorp"])
            await ctx.send(embed=contractEmbed)


def setup(client):
    client.add_cog(PushX(client))
