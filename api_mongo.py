from flask import Flask
from flask_pymongo import PyMongo
from Credentials import constants
import pymongo

app = Flask(__name__)


def unify_db():
    # connecting to mongo
    app.config["MONGO_URI"] = constants.MONGO_CONNECT
    mongo = PyMongo(app)
    # getting the db and disable the SSL certificate for UNIX developers
    db = mongo.init_app(app, tlsAllowInvalidCertificates=True)

    return db


def fetch_Courses():
    db = unify_db()
    courses = db.courses
    cursor = courses.find()
    return cursor


if __name__ == "__main__":
    fetch_Courses()
