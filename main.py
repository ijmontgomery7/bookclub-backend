from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from pymongo import MongoClient
import xml.etree.ElementTree
from model import Book

users =[]
app = Flask(__name__)
api = Api(app)


root = xml.etree.ElementTree.parse('setup.xml').getroot()
for item in root[3]:
        users.append(item.text)

clientURL = 'mongodb+srv://' + root[0].text + ':' + root[1].text + root[2].text


client = MongoClient(clientURL)
books_db = client.db["books"]


bookParser = reqparse.RequestParser()
bookParser.add_argument('user', required=True, type=str, help='the current user selected from dropdown menu')


def clear():
    books_db.drop()


class BookApi(Resource):

    def post(self, bookName):
        args = bookParser.parse_args()
        user = args['user']

        if user not in users:
            return {'status': 'failed user not verified'}

        current = books_db.find_one({'name': bookName})
        if current:
            book = Book(current)
            if user not in book.voters:
                book.addVoter(user, books_db)
                return ({'status': 'success',
                        'message': user + ' has voted for ' + bookName})
            return ({'status': 'failed',
                    'message': 'user has already voted for ' + bookName})
        else:
            book = Book({'voters': [user], 'name': bookName})
            book.save(books_db)
            return ({'status': 'success',
                    'message': 'book ' + bookName + ' submitted'})

    def patch(self, bookName):
        args = bookParser.parse_args()
        user = args['user']

        current = books_db.find_one({'name': bookName})

        if not current:
            abort(404, message='book {} does not exist'.format(bookName))
        book = Book(current)
        if user not in book.voters:
            return {'status': 'failed',
                    'message': 'user has not voted for ' + bookName}
        book.update(books_db, user)
        return {'status': 'success',
                'message': user + ' vote has been removed'}


class BooksApi(Resource):

    def get(self):
        shelf = books_db.find({})
        bookShelf = []
        for book in shelf:
            bookShelf.append(Book(book).__dict__)
        return {'status': 'success', 'books': bookShelf}

class UsersApi(Resource):

    def get(self):
        returnString = []
        for person in users:
            returnString.append(person)
        return {'status': 'successful',
                'users': returnString}


api.add_resource(BookApi, '/shelf/<bookName>')
api.add_resource(BooksApi, '/shelf')
api.add_resource(UsersApi, '/users')

if __name__ == '__main__':
    app.run()
    clear()