import os
import json

class VotingDB:
    def __init__(self, guildID):
        self.__db_file ='{}db.json'.format(guildID)
        if os.path.exists(self.__db_file):
            with open(self.__db_file, 'r') as fp:
                self.__data = json.load(fp)
        else:
            self.__data = {}
        if 'urls' not in self.__data:
            self.__data['urls'] = []
        if 'past_visits' not in self.__data:
            self.__data['past_visits'] = {}

        self.__urls = self.__data['urls']
        self.__past_visits = self.__data['past_visits']
        self.__last_entry = None

    def add(self, url):
        if url not in self.__urls:
            self.__urls.append(url)
            self.__last_entry = url
            with open(self.__db_file, 'w') as fp:
                json.dump(self.__data, fp)
            return True
        else:
            return False

    def forgetLast(self):
        if self.__last_entry is not None:
            self.__urls.remove(self.__last_entry)
            self.__last_entry = None
            return self.__last_entry


    def prepareForVote(self):
        voting_list = []
        max_len = ord('z')-ord('a')
        if len(self.__urls) > max_len:
            voting_list = self.__urls[:max_len]
        else:
            voting_list = self.__urls

        for i, url in enumerate(voting_list):
            emoji = ':regional_indicator_{}:'.format(chr(ord('a')+i))
            yield '{} : {}\n'.format(emoji, url)
        
