

class Book(object):

    def __init__(self, dict):
        self.voters = dict['voters']
        self.name = dict['name']

    def addVoter(self, user, db):
        self.voters.append(user)
        db.insert(self.__dict__)

    def save(self, db):
        db.insert(self.__dict__)

    def update(self, db, user):
        self.voters.remove(user)
        db.update_one({'name': self.name},{"$set": self.__dict__}, upsert=False)

    def delete(self, db):
        db.remove(self.__dict__)
