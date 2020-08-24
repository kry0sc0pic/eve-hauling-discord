from os import environ
from discord import Client, Status, Game , Embed , Color
from redfrogapi import red_frog, black_frog

#token = "" #? Your Bot Token - For running locally
token = environ.get("BOT_TOKEN") #? When deployed on heroku

client = Client()


@client.event
async def on_ready():
    activity = Game(f"on {len(client.servers)} servers", type=3)
    await client.change_presence(status=Status.online, activity=activity)
    print("[READY] Bot is running.....")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
#? Bug Report
    if message.content.startswith("?rfa.reportbug"):
        bugEmbed = Embed(title="Report a bug/issue" , description="Steps to report a bug or an issue with this bot. Use any one method" , colour = Color(0x0f3460))
        bugEmbed.add_field(name="1) Discord Server" , value="You can post a bug on the #bugs-support channel of the discord server(invite below)")
        bugEmbed.add_field(name="2) Github" , value="Make an issue on Github")
        bugEmbed.add_field(name="3) Something you don't want others to know?",value="DM me on discord or send a mail to: krysis21dev@gmail.com")
        bugEmbed.add_field(name="Discord Server Invite" , value="https://discord.gg/FCUEHfK")
        bugEmbed.add_field(name="Github Repo" , value="https://github.com/krishaayjois21/eve-hauling-discord")
        bugEmbed.set_footer(text="Like the bot? , please consider donating ISK to character TitaniumCodex ingame")
        await message.channel.send(content=None,embed=bugEmbed)

#? Bot Help
    if message.content.startswith("?rfa.help"):
        embed = Embed(title="RFA Bot Help" , description="Commands for Red-Frog Bot" , colour = Color(0x0f3460))
        embed.add_field(name="?rf.estimate" ,value="Estimate Costs for Red Frog Freight")
        embed.add_field(name="?bf.estimate" ,value="Estimate Costs for Black Frog Freight")
        embed.add_field(name="?rfa.help" ,value="Displays Help")
        embed.add_field(name="?rfa.reportbug" , value="Report a bug")
        embed.add_field(name="Red Frog Example" , value="?rf.estimate jita->amarr")
        embed.add_field(name="Black Frog Example" , value="?bf.estimate jita->amarr 1000000000")
        embed.set_footer(text="Like the bot? , please consider donating ISK to character TitaniumCodex ingame")
        await message.channel.send(content=None , embed=embed)


#? Red Frog Estimate
    if message.content.startswith("?rf.estimate") or message.content.startswith("?redfrog.estimate"):
        data = {}
        try:
            msg = message.content.strip()
            prefix, systems = msg.split(" ")
            origin, destination = systems.split("->")

            data = red_frog(origin=origin,
                            destination=destination)
            await message.channel.send(
                f"""
**Contract Details**
```
Origin System: {data["origin_name"]}
Destination System: {data["destination_name"]}
Jumps: {data["jumps"]} Jumps
Max Collateral: {data["collateral"]} ISK
Max Volume: {data["volume"]} m3
Normal Reward: {data["reward_base"]} ISK
Rush Reward: {data["reward_rush"]} ISK
Days To Complete: {data["days_to_complete"]}
Expires In (Days): {data["days_expiration"]}
Corp: {data["corporation"]}```
*If you are including containers , put "container" in the contract description and consider a tip.*
"""
            )
        except ValueError:
            await message.send("""
**Error Occurred**
Make Sure you have provided all the details neccessary in this format:
Red Frog: `?rf <origin>-><destination>`
Black Frog: `?bf <origin>-><destination> collateral`
            """)
        except KeyError:
            err = data["error"]
            if err == "Provided collateral exceed our maximum of 25000000000":
                await message.channel.send("Collateral Exceeds maximum amount of 25000000000")
            else:
                await message.channel.send("Star System doesn't exist in RFA Database")
        
        except Exception as e:
            await message.channel.send(
                f"""**An Error Occured**
                ```
                {e}
                ```
                If this occurs repeatedly please report this in the `#bugs-support` channel on this server: 
                https://discord.gg/FCUEHfK
                """
            )

#? Black Frog Estimate

    if message.content.startswith("?bf.estimate") or message.content.startswith("?blackfrog.estimate"):
        try:
            msg = message.content.strip()
            prefix, systems, collateral = msg.split(" ")
            origin, destination = systems.split("->")
            data = black_frog(
                origin=origin, destination=destination, collateral=collateral)
            await message.channel.send(f"""
    **Contract Details**
    ```
    Origin System: {data["origin_name"]}
    Destination System: {data["destination_name"]}
    Distance: {data["distance"]} LY
    Max Collateral: {data["collateral"]} ISK
    Max Volume: {data["volume"]} m3
    Normal Reward: {data["reward_base"]} ISK
    Days To Complete: {data["days_to_complete"]}
    Expires In (Days): {data["days_expiration"]}
    Corp: {data["corporation"]}
    Incursion: {data["has_incursion"]}
    Citadel Service List: {data["service_list_url"]}```
    *If you are including containers , put "container" in the contract description and consider a tip.*
""")
        except ValueError:
            await message.channel.send("""
**Error Occurred**
Make Sure you have provided all the details neccessary in this format:
Red Frog: `?rf <origin>-><destination>`
Black Frog: `?bf <origin>-><destination> collateral`
            """)
        except KeyError:
            err = data["error"]
            if err == "Provided collateral exceed our maximum of 25000000000":
                await message.channel.send("Collateral Exceeds maximum amount of 25000000000 ISK")
            else:
                await message.channel.send("Star System doesn't exist in RFA Database")
 
        except Exception as e:
            await message.channel.send(
                f"""**An Error Occured**
                ```
                {e}
                ```
                If this occurs repeatedly use to `?rsa.reportbug` command to report a bug and include the error message above.
                """
            )



client.run(token)
