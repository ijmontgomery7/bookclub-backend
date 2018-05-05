import requests
import unittest
import xml.etree.ElementTree
from pprint import pprint
from main import clear


def postTest():
    root = xml.etree.ElementTree.parse('setup.xml').getroot()
    user1 = root[3][0].text

    r1 = requests.post('http://127.0.0.1:5000/shelf/Game of Thrones', {'user': user1})
    pprint(r1.json())
    r2 = requests.post('http://127.0.0.1:5000/shelf/Storm of Swords', {'user': user1})
    pprint(r2.json())
    r3 = requests.get('http://127.0.0.1:5000/shelf')
    pprint(r3.json())
    r4 = requests.patch('http://127.0.0.1:5000/shelf/Game of Thrones', {'user': user1})
    pprint(r4.json())
    r5 = requests.get('http://127.0.0.1:5000/shelf')
    pprint(r5.json())
    r6 = requests.get('http://127.0.0.1:5000/users')
    pprint(r6.json())


if __name__ == '__main__':
    clear()
    postTest()

