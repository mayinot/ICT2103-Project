from flask import Flask
from flask_pymongo import PyMongo
from Credentials import constants
import pymongo

app = Flask(__name__)

# connecting to mongo
app.config["MONGO_URI"] = constants.MONGO_CONNECT
mongo = PyMongo(app)
# getting the db and disable the SSL certificate for UNIX developers
mongo.init_app(app, tlsAllowInvalidCertificates=True)


def fetch_Courses() -> object:
    '''

    Args:
        None
    Returns:
        string
    '''

    courses = mongo.db.courses
    cursor = courses.find()
    return cursor


if __name__ == "__main__":
    print(fetch_Courses())
