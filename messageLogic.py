import re
import database
from changelog import ChangeLog

class BotCommand:
    '''Base Bot command. Just dumps command arguments to stdout.'''
    def __init__(self, logic):
        self._logic = logic

    def __call__(self, args):
        print(args)


class HelpCMD(BotCommand):
    '''Prints docstring of all registered commands'''
    def __call__(self, args):
        cmds = self._logic.commands
        return self._logic.__doc__ + '\nAvailable commands:\n' + \
            '\n'.join(['\t**{}{}**: {}'.format(self._logic.command_key, cmd, cmds[cmd].__doc__) for cmd in cmds])

class ForgetCMD(BotCommand):
    '''Remove last newly-added restaurant'''
    def __call__(self, args):
        if isinstance(args, database.VotingDB):
            args.forgetLast()
            return 'Now I remember {} entries'.format(len(args.voting_set))
        else:
            raise TypeError("expecting VotingDB, but got {}".format(args.__class__.__name__))

class VoteCMD(BotCommand):
    '''Output this week's restaurant selection'''
    def __call__(self, args):
        return '\n'.join(s for s in args.prepareForVote())

class ClearCMD(BotCommand):
    '''Remove all saved restaurants'''
    def __call__(self, args):
        l = len(args.voting_set)
        args.voting_set = set()
        return "Removed {} entries".format(l)

class SizeCMD(BotCommand):
    '''Check how many URLs are stored'''
    def __call__(self, args):
        return '{} entries'.format(len(args.voting_set))

class Logic:
    '''I keep track of mentions of restaurants and manage voting of which one to go to'''
    url_re = re.compile('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    command_key = '!'

    def __init__(self, name):
        self.commands = {'help': HelpCMD(self), \
                            'vote': VoteCMD(self), \
                            'clear': ClearCMD(self), \
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

    def restaurant_url_from_message(self, message):
        ''' Get Google Maps url from message containing a restaurant reference '''
        urls = self.url_re.finditer(message)
        for urlgroups in urls:
            url = urlgroups.group()
            if 'maps' in url and 'goo' in url:
                return url

    def is_command(self, message):
        ''' Returns true or false of message is a formal bot command '''
        return message.startswith(self.command_key) and message[len(self.command_key):] in self.commands

    def command_from_message(self, message):
        ''' Returns callable function for a given command '''
        return self.commands[message[len(self.command_key):]]

    