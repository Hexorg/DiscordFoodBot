from git import Repo
import os

class ChangeLog:
    last_announce_file = '.announce'

    def __init__(self):
        self.__repo = Repo('.')
        assert not self.__repo.bare

        self.__announce = ''
        limit_commit = ''
        if os.path.exists(self.last_announce_file):    
            with open(self.last_announce_file, 'r') as f:
                limit_commit = f.read().strip()
        
        pos = 0
        commit = self.__repo.commit('HEAD')
        while commit.hexsha != limit_commit:
            if not commit.message.startswith('Merge'):
                self.__announce += '+ ' + commit.message
            pos += 1
            try:
                commit = self.__repo.commit('HEAD~{}'.format(pos))
            except Exception as e:
                break
        
        with open(self.last_announce_file, 'w') as f:
            f.write(str(self.get_commit()))
            
    def get_commit(self):
        return self.__repo.head.commit
    
    def get_latest_changes(self):
        if len(self.__announce) > 0:
            return '```\n{}\n```'.format(self.__announce)
        else:
            return 'None; just a restart'

    def get_remote(self):
        if len(self.__repo.remotes) > 0:
            return self.__repo.remotes[0].url
        else:
            return 'https://github.com/Hexorg/DiscordFoodBot'