from discord.ext import commands

from database import VotingDB
import messageLogic

bot = commands.Bot(command_prefix='$', description='Test bot')
databases = {}
logics = {}

def init_new_server(guild, bot):
    print('Detected new server - {} (ID: {})'.format(guild.name, guild.id))
    databases[guild.id] = VotingDB()
    logics[guild.id] = messageLogic.Logic(bot.user.name)

@bot.event
async def on_ready():
    print("Logged in as {} ({})".format(bot.user.name, bot.user.id))
    for guild in bot.guilds:
        if guild.id not in databases:
            init_new_server(guild, bot)
        for channel in guild.text_channels:
            if logics[guild.id].should_listen(channel.name):
                await channel.send(logics[guild.id].announce_self())
        

@bot.event
async def on_message(message):
    if message.guild.id not in databases:
        init_new_server(message.guild, bot)
    db = databases[message.guild.id]
    logic = logics[message.guild.id]
    if logic.should_listen(message.channel.name):
        if logic.is_restaurant(message.content):
            response = db.add(logic.restaurant_url_from_message(message.content))
            if response:
                await message.channel.send(response)
        if logic.is_command(message.content):
            command = logic.command_from_message(message.content)
            response = command(db)
            if response:
                await message.channel.send(response)

token=''
with open('token') as f:
    token = f.read().strip()
print('Token is {}'.format(token))
bot.run(token)
