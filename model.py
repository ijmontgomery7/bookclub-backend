

class Book(object):

    def __init__(self, dict):
        self.voters = dict['voters']
        self.name = dict['name']

    def addVoter(self, user, db):
        self.voters.append(user)
        db.insert(self.__dict__)

    def save(self, db):
        db.insert(self.__dict__)


