
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
    query = {"AvgGradPay": "N.A"}
    update_dataset = {"$set": {"AvgGradPay": "0"}}
    update_data = api_mongo.mongo.db.courses
    update_data.update_many(query, update_dataset)


if __name__ == "__main__":
    emergency_update()
