from flask import Flask
from flask import request, flash, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo import cursor
from Credentials import constants
import pymongo

app = Flask(__name__)


# connecting to mongo
app.config["MONGO_URI"] = constants.MONGO_CONNECT
mongo = PyMongo(app)
# getting the db and disable the SSL certificate for UNIX developers
db = mongo.init_app(app, tlsAllowInvalidCertificates=True)


def fetch_Courses() -> object:
    '''
    Queries univeristy courses dataset from database

    Args:
        None
    Returns:
        cursor (object): queried dataset object address
    '''

    courses = mongo.db.courses
    cursor = courses.find()
    return cursor


def fetch_Uninames():
    courses = mongo.db.courses
    cursor = courses.distinct("University.UniName")
    return cursor


def fetch_CategoryNames():
    category = mongo.db.category
    courses = mongo.db.courses
    cursor = category.distinct("CategoryName")
    return cursor


def filter_Course(UniList, category_name, FROMsalary, TOsalary):
    if TOsalary < FROMsalary:
        flash('To Salary cannot be more than From Salary!')
        redirect(url_for('courses'))
    category = mongo.db.category
    courses = mongo.db.courses
    join_collection = courses.aggregate([{"$lookup": {"from": "category", "localField": "Faculty.CategoryID", "foreignField": "CategoryID", "as": "Category_Info"}},
                                         {"$match": {"Category_Info": {"$elemMatch": {"CategoryName": category_name}}, "AvgGradPay": {"$gte": FROMsalary, "$lte": TOsalary}, "University.UniName": {"$in": UniList}}}])
    return join_collection


def top_salary() -> object:
    courses = mongo.db.courses
    query = {}
    projection = {}
    # cur = courses.find(query, projection)
    cur = list(courses.find())
    return cur


if __name__ == "__main__":
    # print statement here to test out whether API is working and what object is returning
    # just type python api_mongo.py in the cmd.
    # print(fetch_Courses())
    # filter_Course(UniList, category_name, FROMsalary, TOsalary)
    print(top_salary())
    pass
