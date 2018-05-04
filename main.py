from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from pymongo import MongoClient
import xml.etree.ElementTree
from model import Book, User

app = Flask(__name__)
api = Api(app)


root = xml.etree.ElementTree.parse('setup.xml').getroot()


clientURL = 'mongodb+srv://' + root[0].text + ':' + root[1].text + root[2].text

# limit inputs so site doesnt get spammed
limit = int(root[4].text)

books_db = MongoClient(clientURL).db["books"]
user_db = MongoClient(clientURL).db["users"]

for item in root[3]:
        user_db.insert({'name': item.text, 'proposed': 0})

bookParser = reqparse.RequestParser()
bookParser.add_argument('user', required=True, type=str, help='the current user selected from dropdown menu')


def clear():
    books_db.drop()
    user_db.drop()


class BookApi(Resource):

    def post(self, bookName):
        args = bookParser.parse_args()

        user = User(user_db.find_one({'name': args['user']}))
        if not user:
            abort(404, message=user.name + 'not found')

        current = books_db.find_one({'name': bookName})
        if current:
            book = Book(current)
            if user in book.voters:
                abort(400, message='user has already voted for ' + bookName)
            book.addVoter(user, books_db)
            return {'message': user.name + ' has voted for ' + bookName}

        else:
            if user.proposed <= limit:

                book = Book({'voters': [user.name], 'name': bookName, 'proposer': user})
                User.propose()
                book.save(books_db)
                return {'message': 'book ' + bookName + ' submitted'}
            else:
                abort(400, message=user.name + 'has suggested too many books')

    def patch(self, bookName):
        args = bookParser.parse_args()
        user = args['user']

        current = books_db.find_one({'name': bookName})

        if not current:
            abort(404, message='book {} does not exist'.format(bookName))

        book = Book(current)
        if user not in book.voters:
            abort(400, message='user has not voted for ' + bookName)

        book.update(books_db, user)
        return {'message': user + ' vote has been removed'}


    def delete(self, bookName):
        current = books_db.find_one({'name': bookName})
        if not current:
            abort(404, message=bookName + ' not found')
        book = Book(current)
        if len(book.voters) > 0:
            abort(400, message=bookName + ' has voters left')
        owner = User(user_db.find_one({'name': book.proposer}))
        owner.proposed += 1
        owner.update(user_db)
        book.delete(books_db)
        return {'message': bookName + ' has been deleted'}

class BooksApi(Resource):

    def get(self):
        return{books_db.find({})}


class UsersApi(Resource):

    def get(self):
        return {'users': user_db.find({})}

api.add_resource(BookApi, '/shelf/<bookName>')
api.add_resource(BooksApi, '/shelf')
api.add_resource(UsersApi, '/users')

if __name__ == '__main__':
    app.run()
    clear()