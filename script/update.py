
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
    query = {    "University": {
        "UniName": "Singapore University of Technology and Design",
        "UniAbb": "SUTD",
        "UniDesc": "SUTD is established to advance knowledge and nurture technically grounded leaders and innovators to serve societal needs.",
        "UniImage": "https://istd.sutd.edu.sg/files/xsutd-istd-logo-web-2021.png.pagespeed.ic.eScdBEiZXf.png"
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
