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

def fetch_UniversityNames():
    db = unify_db()
    univeristy = db.courses
    cursor = univeristy.distinct("University.UniName")
    return cursor

    
def fetch_CategoryNames():
    db = unify_db()
    courses = db.courses
    category = db.category
    category_name = category.distinct("CategoryName")
    join_collection = courses.aggregate([{"$lookup": { "from": "category", "localField": "Faculty.CategoryID", "foreignField": "CategoryID", "as": "Category_Info" }}, { "$match": {"University.UniName":"Singapore Management University" }}])
    return join_collection

if __name__ == "__main__":
    fetch_Courses()
