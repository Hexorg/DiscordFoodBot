import re
import database
from changelog import ChangeLog

class BotCommand:
    '''Base Bot command. Just dumps command arguments to stdout.'''
    def __init__(self, logic):
        self._logic = logic

    def __call__(self):
        print('{} is called'.format(self.__class__.__name__))


class HelpCMD(BotCommand):
    '''Prints docstring of all registered commands'''
    def __call__(self):
        cmds = self._logic.commands
        return self._logic.__doc__ + '\nAvailable commands:\n' + \
            '\n'.join(['\t**{}{}**: {}'.format(self._logic.command_key, cmd, cmds[cmd].__doc__) for cmd in cmds])

class ForgetCMD(BotCommand):
    '''Remove last newly-added restaurant'''
    def __call__(self):
        url = self._logic.database.forgetLast()
        if url:
            return '{} has been removed from the database'.format(url)

class VoteCMD(BotCommand):
    '''Output this week's restaurant selection'''
    def __call__(self):
        return [s for s in self._logic.database.prepareForVote()]

class VoteEndCMD(BotCommand):
    '''Tally up the votes and tell us where we are going'''
    def __call__(self):
        pass


class SizeCMD(BotCommand):
    '''Check how many URLs are stored'''
    def __call__(self):
        return '{} entries'.format(len(args.voting_set))

class Logic:
    '''I keep track of mentions of restaurants and manage voting of which one to go to'''
    url_re = re.compile('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    command_key = '!'

    def __init__(self, name, guildId):
        self.database = database.VotingDB(guildId)
        self.commands = {'help': HelpCMD(self), \
                            'vote': VoteCMD(self), \
                            'endvote': VoteEndCMD(self), \
                            'size': SizeCMD(self), \
                            'forget': ForgetCMD(self)}
        self.__changelog = ChangeLog()
        
        self.name = name

    def should_listen(self, channel):
        ''' Returns true or false, if bot should listen on this channel '''
        return channel == 'dinner-organization'
    
    def announce_self(self):
        return "Greetings! New {} is up! From commit {}.\nLatest changes:\n{}\nAs usual, for new feature requests, add issues to {}".format( \
            self.name, str(self.__changelog.get_commit())[:7], self.__changelog.get_latest_changes(), \
            self.__changelog.get_remote())

    def is_restaurant(self, message):
        ''' Returns true or false if message contains a restaurant reference '''
        urls = self.url_re.finditer(message)
        for urlgroups in urls:
            url = urlgroups.group()
            if 'maps' in url and 'goo' in url:
                return True
        return False

    def add(self, message):
        ''' Add a restaurant reference '''
        urls = self.url_re.finditer(message)
        for urlgroups in urls:
            url = urlgroups.group()
            if 'maps' in url and 'goo' in url:
                isAddedNew = self.database.add(url)
                if isAddedNew:
                    return "New restaurant added."
                else:
                    return "This restaurant is already in the database"

    def is_command(self, message):
        ''' Returns true or false of message is a formal bot command '''
        return message.startswith(self.command_key) and message[len(self.command_key):] in self.commands

    def command_from_message(self, message):
        ''' Returns callable function for a given command '''
        return self.commands[message[len(self.command_key):]]

    