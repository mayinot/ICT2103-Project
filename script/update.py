
from flask_pymongo import PyMongo
import os
import sys

path_dir = os.path.abspath('..')
sys.path.insert(1, path_dir)
import api_mongo
'''
This scripts are mainly to update and fix errors in the dataset,
Do tweak the variables in your accordance
'''


def emergency_update():
    query = {"University": {
        "UniName": "Singapore Institute of Technology",
        "UniAbb": "SIT",
        "UniDesc": "Singapore Institute of Technology (SIT) is Singapore’s university of applied learning. SIT’s vision is to be a leader in innovative learning by integrating learning, industry and community. Its mission is to nurture and develop individuals who build on their interests and talents to impact society in meaningful ways.",
        "UniImage": "https://digitalsenior.sg/wp-content/uploads/2013/10/SIT-logo.jpg"
    }}
    update_dataset = {"$set": {"GradeProfile": {
        "Poly10thPerc": "N.A",
        "Poly90thPerc": "N.A",
        "Alevel10thPerc": "N.A",
        "Alevel90thPerc": "N.A"
    }}}
    update_data = api_mongo.mongo.db.courses
    update_data.update_many(query, update_dataset)


if __name__ == "__main__":
    emergency_update()
