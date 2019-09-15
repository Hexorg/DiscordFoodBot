import re
import database

class BotCommand:
    def __init__(self, logic):
        self.__logic = logic

    def __call__(self, args):
        print(args)
    
    def about(self):
        return "Base Bot command. Just dumps command arguments to stdout."

class HelpCMD(BotCommand):
    pass

class Logic:
    url_re = re.compile('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    command_key = '!'

    def __init__(self):
        self.commands = {'help': HelpCMD(self)}

    def should_listen(self, channel):
        ''' Returns true or false, if bot should listen on this channel '''
        return channel == 'dinner-organization'

    def is_restaurant(self, message):
        ''' Returns true or false if message contains a restaurant reference '''
        urls = url_re.finditer(message)
        for urlgroups in urls:
            url = urlgroups.group()
            if 'maps' in url and 'goo' in url:
                return True
        return False

    def restaurant_url_from_message(self, message):
        ''' Get Google Maps url from message containing a restaurant reference '''
        urls = url_re.finditer(message)
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

    