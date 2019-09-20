from discord.ext import commands
import messageLogic

bot = commands.Bot(command_prefix='$', description='Test bot')
logics = {}

def init_new_server(guild, bot):
    print('Detected new server - {} (ID: {})'.format(guild.name, guild.id))
    logics[guild.id] = messageLogic.Logic(bot.user.name, guild.id)

@bot.event
async def on_ready():
    print("Logged in as {} ({})".format(bot.user.name, bot.user.id))
    for guild in bot.guilds:
        if guild.id not in logics:
            init_new_server(guild, bot)
        for channel in guild.text_channels:
            if logics[guild.id].should_listen(channel.name):
                await channel.send(logics[guild.id].announce_self())
        

@bot.event
async def on_message(message):
    logic = logics[message.guild.id]
    if logic.should_listen(message.channel.name) and message.author != bot.user:
        if logic.is_restaurant(message.content):
            response = logic.add(message.content)
        if logic.is_command(message.content):
            command = logic.command_from_message(message.content)
            response = command()
        
        if response:
            if isinstance(response, list):
                for msg in response:
                    await message.channel.send(msg)
            else:
                await message.channel.send(response)

token=''
with open('token') as f:
    token = f.read().strip()
print('Token is {}'.format(token))
bot.run(token)
