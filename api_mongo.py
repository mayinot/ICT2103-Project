from flask import Flask
from flask_pymongo import PyMongo
from Credentials import constants
import pymongo

app = Flask(__name__)


def test_db():
    client = pymongo.MongoClient(constants.MONGO_CONNECT)
    db = client.test
    print("works good")


if __name__ == "__main__":
    test_db()
