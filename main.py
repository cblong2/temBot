import discord
import os
import requests
import json
import random
from discord.ext import commands
from replit import db

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# client = discord.Client(intents=intents)
my_secret = os.environ['TOKEN']


def boldText(txt):
    if isinstance(txt, str):
        return '**' + txt + '**'
    else:
        return '**' + str(txt) + '**'


def checkTemExist(name="", number=0):
    if "TemTem" in db.keys():
        if number != 0:
            if str(number) in db["TemTem"]:  # Checking based on number
                print("Found " + str(number) + " in db!")
                return db["TemTem"][str(number)]
            else:
                print(f'TemTem with {number} not in db!')
                response = requests.get(
                    "https://temtem-api.mael.tech/api/temtems/" + str(number))
                json_data = json.loads(response.text)
                db["TemTem"][str(number)] = json_data
                # print(json_data)
                return json_data

        elif name != "":
            for tem in db["TemTem"]:  # Checking based on name
                # print(db["TemTem"][tem])
                if db["TemTem"][tem]["name"] == name:
                    print(f'Found {name} in db!')
                    return db["TemTem"][tem]
            print(f'TemTem with {name} not in db!')
            response = requests.get("https://temtem-api.mael.tech/api/temtems",
                                    params={'names': [name]})
            json_data = json.loads(response.text)
            # print(json_data[]0)
            db["TemTem"][json_data[0]["number"]] = json_data[0]
            return json_data[0]
    else:
        print("Database does not exist")
        db["TemTem"] = {}  # JSON Object
        if number != 0:
            response = requests.get(
                "https://temtem-api.mael.tech/api/temtems/" + str(number))
            json_data = json.loads(response.text)
            db["TemTem"][str(number)] = json_data
            return json_data
        else:
            response = requests.get("https://temtem-api.mael.tech/api/temtems",
                                    params={'names': [name]})
            json_data = json.loads(response.text)
            # print(json_data[]0)
            db["TemTem"][json_data[0]["number"]] = json_data[0]
            return json_data[0]


def embedTem(jsonTem):
    embed = discord.Embed(title=jsonTem["name"],
                          url=jsonTem["wikiUrl"],
                          description=jsonTem["gameDescription"],
                          color=0x9466de)
    embed.set_thumbnail(url=jsonTem["portraitWikiUrl"])
    embed.add_field(
        name="Traits",
        value=
        f'Trait 1: {boldText(jsonTem["traits"][0])}\nTrait 2: {boldText(jsonTem["traits"][1])}'
    )
    embed.add_field(name="Stats",
                    value=f'HP: {boldText(jsonTem["stats"]["hp"])}\n\
                    STA: {boldText(jsonTem["stats"]["sta"])}\n\
                    SPD: {boldText(jsonTem["stats"]["spd"])}\n\
                    ATK: {boldText(jsonTem["stats"]["atk"])}\n\
                    DEF: {boldText(jsonTem["stats"]["def"])}\n\
                    SPATK: {boldText(jsonTem["stats"]["spatk"])}\n\
                    SPDEF: {boldText(jsonTem["stats"]["spdef"])}')
    return embed


# <PROTOTYPE FUNCTION>
# Use this function as a template in finding and returning information about a particular TemTem.
def getRandTem():
    i = random.randint(1, 164)
    
    # response = requests.get("https://temtem-api.mael.tech/api/temtems")
    # json_data = json.loads(response.text)
    jsonTem = checkTemExist(number=i)
    # print(json_data)
    # temUrl = json_data[i]["wikiUrl"]
    # temName = json_data[i]["name"]

    return embedTem(jsonTem)


def getTem(name):
    jsonTem = checkTemExist(name=name)
    return embedTem(jsonTem)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         # await message.channel.send('You Big Dummy!')
#         return

#     if message.content.startswith('$hello'):
#         print("Received a command")
#         await message.channel.send(f'Hello {message.author}!')
'''
discord.Member   - Case Sensitive name of user name
error            - Class / Callback of some sorts, use error.__class__.__name__ to get the actual name. 
                   When casted to a string, the error message appears.
ctx              - Possibly the equivalent to message.channel?

'''


@bot.command(
)  # Event for a command with the same name as the function defined below.
async def tem(ctx, name):
    print("Received [tem] command")
    await ctx.send(embed=getTem(name))
    # await ctx.send(f'Your random tem is {get_tem()}!')


@bot.command(
)  # Event for a command with the same name as the function defined below.
async def randtem(ctx):
    print("Received [randtem] command")
    await ctx.send(embed=getRandTem())
    # await ctx.send(f'Your random tem is {get_tem()}!')


@bot.command(
)  # Event for a command with the same name as the function defined below.
async def hello(ctx, *, member: discord.Member):
    print("Received a command")
    await ctx.send(f'Hello {member}!')


@hello.error
async def hello_error(ctx, error):
    print("Error type: " + str(error.__class__.__name__))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('I could not find that member...')


@bot.command()
async def info(ctx, *, member: discord.Member):
    """Tells you some info about the member."""
    print("Info Requested")
    msg = f'{member} joined on {member.joined_at} and has {len(member.roles)} roles.'
    await ctx.send(msg)


@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')


db.clear()
bot.run(my_secret)  # Calls and starts the bot process
# client.run(my_secret)     # Not used since we are using the bot framework
