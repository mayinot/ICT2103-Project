from flask import Flask
from flask_pymongo import PyMongo
from Credentials import constants
import pymongo

app = Flask(__name__)


def unify_db():
    #connecting to mongo
    client = pymongo.MongoClient(constants.MONGO_CONNECT)
    #getting the db
    db = client.unify_db
    return db

def fetch_Courses():
    db = unify_db()
    courses = db.courses
    cursor = courses.find()
    return cursor

def fetch_CategoryNames():
    db = unify_db()
    category = db.category
    cursor = category.distinct("CategoryName")
    return cursor

def fetch_UniversityNames():
    db = unify_db()
    univeristy = db.courses
    cursor = univeristy.distinct("University.UniName")
    return cursor

if __name__ == "__main__":
    fetch_Courses()
