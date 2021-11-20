from flask import Flask
from flask import request, flash, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from Credentials import constants
import pymongo

app = Flask(__name__)

# connecting to mongo
app.config["MONGO_URI"] = constants.MONGO_CONNECT
mongo = PyMongo(app)
# getting the db and disable the SSL certificate for UNIX developers
mongo.init_app(app, tlsAllowInvalidCertificates=True)

# connecting to mongo
app.config["MONGO_URI"] = constants.MONGO_CONNECT
mongo = PyMongo(app)
# getting the db and disable the SSL certificate for UNIX developers
db= mongo.init_app(app, tlsAllowInvalidCertificates=True)




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
    '''
    Query to get all the universities

    Args:
        connection_string (MySQLConnection): The database location mysql connector
    Returns:
        uniFilter (list): a list of tuples representing the queried payload   
    '''
    univeristy = mongo.db.courses
    uniFilter = univeristy.distinct("University.UniName")
    return uniFilter

def fetch_CategoryNames():
    category = mongo.db.category
    courses = mongo.db.courses
    cursor = category.distinct( "CategoryName")
    return cursor

def fetch_CategoryNames(getUniCat):
    '''
    Query to get all the categories according to the selected university

    Args:
        getUniCat: get the selected university
    Returns:
        list: a list of tuples representing the queried payload 
    '''
    courses = mongo.db.courses
    category = mongo.db.category
    category_name = category.distinct("CategoryName")
    join_collection = courses.aggregate([{"$lookup": { "from": "category", "localField": "Faculty.CategoryID", "foreignField": "CategoryID", "as": "Category_Info" }}, { "$match": { "Category_Info": { "$elemMatch": { "University.UniName" : { "$in": getUniCat }}  }}}])
    return join_collection

def filter_Course(UniList, category_name, FROMsalary, TOsalary):
    if TOsalary < FROMsalary:
            flash('To Salary cannot be more than From Salary!')
            redirect(url_for('courses'))
    category = mongo.db.category
    courses = mongo.db.courses
    join_collection = courses.aggregate([{"$lookup": { "from": "category", "localField": "Faculty.CategoryID", "foreignField": "CategoryID", "as": "Category_Info" }}, 
    { "$match": { "Category_Info": { "$elemMatch": { "CategoryName": category_name }}, "AvgGradPay": { "$gte": FROMsalary, "$lte": TOsalary}, "University.UniName" : { "$in": UniList } }}])
    return join_collection
    
if __name__ == "__main__":
    fetch_Courses()
    filter_Course(UniList, category_name, FROMsalary, TOsalary)

