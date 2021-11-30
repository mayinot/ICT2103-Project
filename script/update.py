
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


def single_query():
    q = { }
    pro = {"Intake": 1, "_id": 1}
    find = api_mongo.mongo.db.courses
    single = find.find(q, pro)
    return list(single)

def emergency_update():
    update_data = api_mongo.mongo.db.courses
    for i in range(140):
        query = {"_id": single_query()[i]['_id'], "Intake": single_query()[i]['Intake']}      
        update_dataset = {"$set": {"Intake": int(single_query()[i]['Intake'])}}
        update_data.update_one(query, update_dataset)


if __name__ == "__main__":
   emergency_update()
   