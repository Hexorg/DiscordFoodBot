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
        
