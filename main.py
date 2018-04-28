from flask import Flask
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import xml.etree.ElementTree
from model import Book

users =[]
app = Flask(__name__)
api = Api(app)
db = None


root = xml.etree.ElementTree.parse('setup.xml').getroot()
for item in root[3]:
        users.append(item.text)

clientURL = 'mongodb+srv://' + root[0].text + ':' + root[1].text + root[2].text


client = MongoClient(clientURL)
db = client.db["books"]







bookPostParser = reqparse.RequestParser()
bookPostParser.add_argument('user', required=True, type=str, help='the current user selected from dropdown menu')
bookPostParser.add_argument('book', required=True, type=str, help='the book that is being added or voted on')


class BookApi(Resource):


    def post(self):
        args = bookPostParser.parse_args()
        user = args['user']
        bookName = args['book']

        if user not in users:
            return {'status': 'failed user not verified'}

        current = db.find_one({'name': bookName})
        if current:
            book = Book(current)
            if user not in book.voters:
                book.addVoter(user, db)
                return ({'status': 'success',
                        'message': user + ' has voted for ' + bookName})
            return ({'status': 'failed',
                    'message': 'user has already voted for ' + bookName})
        else:
            book = Book({'voters': [user], 'name': bookName})
            book.save(db)
            return ({'status': 'success',
                    'message': 'book ' + bookName + ' submitted'})

    def get(self):
        shelf = db.find({})
        return {'status': 'success', 'books': shelf}

api.add_resource(BookApi, '/shelf')

if __name__ == '__main__':
    app.run()