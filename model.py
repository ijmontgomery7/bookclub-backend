

class Book(object):

    def __init__(self, dict):
        self.voters = dict['voters']
        self.name = dict['name']
        self.proposer = dict['proposer']

    def addVoter(self, user, db):
        self.voters.append(user.name)
        db.insert(self.__dict__)

    def save(self, db):
        db.insert(self.__dict__)

    def update(self, db, user):
        self.voters.remove(user)
        db.update_one({'name': self.name},{"$set": self.__dict__}, upsert=False)

    def delete(self, db):
        db.remove(self.__dict__)


class User(object):

    def __init__(self, dict):
        self.name = dict['name']
        self.proposed = dict['proposed']

    def propose(self):
        self.proposed += 1

    def save(self, db):
        db.insert(self.__dict__)

    def update(self, db):
        db.update_one({'name': self.name}, {"$set": self.__dict__}, upsert=False)

