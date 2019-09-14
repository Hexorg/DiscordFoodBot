from discord.ext import commands
import re

class VotingDB:
    def __init__(self):
        self.voting_set = set()
        self.last_entry = None

    def add(self, url):
        if url not in self.voting_set:
            self.voting_set.add(url)
            self.last_entry = url
            response = "New location is added to the voting set. New set size is {}".format(len(self.voting_set))
            return response

    def forgetLast(self):
        if self.last_entry is not None:
            self.voting_set.remove(self.last_entry)

    def prepareForVote(self):
        for i, url in enumerate(self.voting_set):
            emoji = ':regional_indicator_{}:'.format(chr(ord('a')+i))
            yield '{} : {}\n'.format(emoji, url)
        


url_re = re.compile('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
bot = commands.Bot(command_prefix='$', description='Test bot')
votingDB = VotingDB()

@bot.event
async def on_ready():
    print("Logged in as {} ({})".format(bot.user.name, bot.user.id))

@bot.event
async def on_message(message):
    if message.channel.name == 'dinner-organization':
        urls = url_re.finditer(message.content)
        for urlgroups in urls:
            url = urlgroups.group()
            if 'maps' in url and 'goo' in url:
                response = votingDB.add(url)            
                if response:
                    await message.channel.send(response)
        if message.content.startswith('!vote'):
            for msg in votingDB.prepareForVote():
                await message.channel.send(msg)
        elif message.content.startswith('!clear'):
            votingDB.voting_set = set()
            await message.channel.send('Deleted')

        elif message.content.startswith('!size'):
            await message.channel.send('There are {} location entries right now'.format(len(votingDB.voting_set)))
        elif message.content.startswith('!forget'):
            votingDB.forgetLast()
            await message.channel.send('Done. There are {} location entries right now'.format(len(votingDB.voting_set)))
        elif message.content.startswith('!help'):
            await message.channel.send('I look for google maps urls and catalogie them.\n\t!vote - Display all stored URLs\n\t!clear - Remove all URLs\n\t!size - check how many URLs are stored\n\t!forget - Remove the last entered URL\n\t!help - Display this text')
token=''
with open('token') as f:
    token = f.read().strip()
print('Token is {}'.format(token))
bot.run(token)
