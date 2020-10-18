import discord
from discord.ext import commands


class List(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def list(self, ctx):
        with open("./services/services.txt", "r") as services:
            await ctx.send(
                f"""**Supported Services:**\n
```{services.read()}```
            
""")


def setup(client):
    client.add_cog(List(client))
