import discord
import os
import requests
import json
import random
from discord.ext import commands

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

# <PROTOTYPE FUNCTION>
# Use this function as a template in finding and returning information about a particular TemTem.
def get_tem():
    response = requests.get("https://temtem-api.mael.tech/api/temtems")
    json_data = json.loads(response.text)
    i = random.randint(0, len(json_data) - 1)
    # temUrl = json_data[i]["wikiUrl"]
    # temName = json_data[i]["name"]
    embed = discord.Embed(title=json_data[i]["name"],
                          url=json_data[i]["wikiUrl"],
                          description=json_data[i]["gameDescription"],
                          color=0x9466de)
    embed.set_thumbnail(url=json_data[i]["portraitWikiUrl"])
    embed.add_field(
        name="Traits",
        value=
        f'Trait 1: {boldText(json_data[i]["traits"][0])}\nTrait 2: {boldText(json_data[i]["traits"][1])}'
    )
    embed.add_field(name="Stats",
                    value=f'HP: {boldText(json_data[i]["stats"]["hp"])}\n\
                      STA: {boldText(json_data[i]["stats"]["sta"])}\n\
                      SPD: {boldText(json_data[i]["stats"]["spd"])}\n\
                      ATK: {boldText(json_data[i]["stats"]["atk"])}\n\
                      DEF: {boldText(json_data[i]["stats"]["def"])}\n\
                      SPATK: {boldText(json_data[i]["stats"]["spatk"])}\n\
                      SPDEF: {boldText(json_data[i]["stats"]["spdef"])}')
    return embed


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
async def randtem(ctx):
    print("Received [randtem] command")
    await ctx.send(embed=get_tem())
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


bot.run(my_secret)  # Calls and starts the bot process
# client.run(my_secret)     # Not used since we are using the bot framework
