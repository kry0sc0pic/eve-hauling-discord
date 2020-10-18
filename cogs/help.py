from discord.ext import commands
import discord
class Help(commands.Cog):
    def __init__(self , client):
        self.client = client

    @commands.command()
    async def help(self , ctx):
        embed = discord.Embed(
            title="EVE Hauling Bot Help",
            description="Help for the EVE hauling bot",
            color=discord.Color.from_rgb(214, 224, 240)
        )
        embed.add_field(name="Prefix", value="The Prefix is `?`", inline=False)
        embed.add_field(name="list", value="Lists all the supported freight services supported")
        embed.add_field(name="calculate", value="replace <service_name> with the service name and follow the example")
        embed.add_field(name="info", value="Get information about a supported service , check example below")
        embed.add_field(name="example(calculate):",
                        value="<service_name> `origin_system` `destination_system` `collateral` `volume`", inline=False)
        embed.add_field(name="example(info):", value="?info `service_name`", inline=False)
        embed.set_thumbnail(url="https://images.evetech.net/types/28844/render")
        embed.set_footer(text="Like the bot? Consider supporting the bot by sending ISK to `TitaniumCodex` ingame")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))