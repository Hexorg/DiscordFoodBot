from discord.ext import commands

from database import VotingDB
import messageLogic

bot = commands.Bot(command_prefix='$', description='Test bot')
databases = {}
logics = {}

@bot.event
async def on_ready():
    print("Logged in as {} ({})".format(bot.user.name, bot.user.id))

@bot.event
async def on_message(message):
    if message.guild.id not in databases:
        print('Detected new server - {} (ID: {})'.format(message.guild.name, message.guild.id))
        databases[message.guild.id] = VotingDB()
        logics[message.guild.id] = messageLogic.Logic()
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
