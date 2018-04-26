from flask_restful import fields


class Book(object):

    resource_fields = {
        'name': fields.String,
        'voters': fields.List
    }

    def __init__(self, name, creator):
        self.voters = [creator]
        self.name = name

    def getVote(self):
        return len(self.voters)

    def addVoter(self, user):
        if user not in self.voters:
            self.voters.append(user)


class Shelf(object):

    resource_fields = {
        'shelf': fields.Nested
    }

    def __init__(self):
        self.shelf = {}

    def addBook(self, book):
        if book.name not in self.shelf:
            self.shelf[book.name] = book

    def getBooks(self):
        return self.shelf
