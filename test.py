import requests
import unittest
import xml.etree.ElementTree
from pprint import pprint


def postTest():
    root = xml.etree.ElementTree.parse('setup.xml').getroot()
    user1 = root[3][0].text

    r1 = requests.post('http://127.0.0.1:5000/shelf', {'user': user1, 'book': 'Game of Thrones'})
    pprint(r1.json())
    r2 = requests.post('http://127.0.0.1:5000/shelf', {'user': user1, 'book': 'Storm of Swords'})
    pprint(r2.json())

if __name__ == '__main__':
    postTest()