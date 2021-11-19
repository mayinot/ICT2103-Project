from flask import request, flash, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from Credentials import constants
import pymongo




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

def fetch_Uninames():
    db = unify_db()
    courses = db.courses
    cursor = courses.distinct( "University.UniName")
    return cursor

def fetch_CategoryNames():
    db = unify_db()
    category = db.category
    courses = db.courses
    cursor = category.distinct( "CategoryName")
    return cursor

def filter_Course(UniList, category_name, FROMsalary, TOsalary):
    if TOsalary < FROMsalary:
            flash('To Salary cannot be more than From Salary!')
            redirect(url_for('courses'))
    db = unify_db()
    courses = db.courses
    category = db.category
    print(UniList)
    join_collection = courses.aggregate([{"$lookup": { "from": "category", "localField": "Faculty.CategoryID", "foreignField": "CategoryID", "as": "Category_Info" }}, { "$match": { "Category_Info": { "$elemMatch": { "CategoryName": category_name }}, "AvgGradPay": { "$gte": FROMsalary, "$lte": TOsalary}, "University.UniName" : { "$in": UniList } }}])
    return join_collection
    
if __name__ == "__main__":
    fetch_Courses()
    filter_Course(UniList, category_name, FROMsalary, TOsalary)
