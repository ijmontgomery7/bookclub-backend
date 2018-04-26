from flask import Flask
from flask_restful import Resource, Api, marshal_with
from pymongo import MongoClient
import xml.etree.ElementTree
import model
from pprint import pprint

root = xml.etree.ElementTree.parse('setup.xml').getroot()

clientURL = 'mongodb+srv://' + root[0].text + ':' + root[1].text + root[2].text

client = MongoClient(clientURL)

app = Flask(__name__)
api = Api(app)


class Bookshelf(Resource):

    shelf = model.Shelf()



if __name__ == '__main__':
    app.run(debug=True)