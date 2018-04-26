from pymongo import MongoClient
import xml.etree.ElementTree
from pprint import pprint

root = xml.etree.ElementTree.parse('setup.xml').getroot()

clientURL = 'mongodb+srv://' + root[0].text + ':' + root[1].text + root[2].text

client = MongoClient(clientURL)

db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)