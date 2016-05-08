#!/usr/bin/env python

"""
# Run this program
export COMPOSE_FILE=docker-compose-shard.yml
docker-compose run --rm --no-deps cli python /scripts/install_shard.py

# All remove
docker-compose down -v --rmi local
"""

import sys
import time
import os

from pymongo import MongoClient

class constants:
    MONGODB_URL = os.environ.get("WIDUKIND_MONGODB_URL", "mongodb://localhost/widukind")
    COL_CATEGORIES = "categories"
    COL_CALENDARS = "calendars"
    COL_PROVIDERS = "providers"
    COL_DATASETS = "datasets"
    COL_SERIES = "series"
    COL_TAGS = "tags"
    COL_LOCK = "lock"
    COL_COUNTERS = "counters"
    COL_QUERIES = "queries"
    COL_LOGS = "logs"

def abort():
    print("program aborted...")
    sys.exit(1)

def create_or_update_indexes(db, force_mode=False, background=False):

    db[constants.COL_CALENDARS].create_index([
        ("key", ASCENDING)], 
        name="key_idx", unique=True, background=background)

    db[constants.COL_PROVIDERS].create_index([
        ("slug", ASCENDING)], 
        name="slug_idx", unique=True, background=background)

    db[constants.COL_PROVIDERS].create_index([
        ("name", ASCENDING)], 
        name="name_idx", 
        background=background)

    db[constants.COL_CATEGORIES].create_index([
        ("slug", ASCENDING)], 
        name="slug_idx", unique=True, background=background)

    db[constants.COL_CATEGORIES].create_index([
        ('provider_name', ASCENDING), 
        ("category_code", ASCENDING)], 
        name="provider_category_idx", 
        #unique=True, 
        background=background)
    
    db[constants.COL_CATEGORIES].create_index([
        ("tags", ASCENDING)], 
        name="tags_idx", background=background)

    db[constants.COL_DATASETS].create_index([
        ("slug", ASCENDING)], 
        name="slug_idx", unique=True, background=background)

    db[constants.COL_DATASETS].create_index([
        ("tags", ASCENDING)], 
        name="tags_idx", background=background)
    
    db[constants.COL_DATASETS].create_index([
        ('provider_name', ASCENDING), 
        ("dataset_code", ASCENDING)], 
        name="datasets1", 
        background=background)

    db[constants.COL_DATASETS].create_index([
        ('provider_name', ASCENDING), 
        ("dataset_code", ASCENDING),
        ("tags", ASCENDING)], 
        name="datasets2", background=background)

    db[constants.COL_DATASETS].create_index([
        ("last_update", ASCENDING)], 
        name="datasets3")

    db[constants.COL_SERIES].create_index([
        ("slug", ASCENDING)], 
        name="slug_idx", unique=True, background=background)

    db[constants.COL_SERIES].create_index([
        ('provider_name', ASCENDING), 
        ("dataset_code", ASCENDING), 
        #("key", ASCENDING)
        ], 
        name="series1", 
        background=background)

    db[constants.COL_SERIES].create_index([
        ("dimensions", ASCENDING)], 
        name="series2", background=background)

    db[constants.COL_SERIES].create_index([
        ("attributes", ASCENDING)], 
        name="series3", background=background)

    db[constants.COL_SERIES].create_index([
        ("tags", ASCENDING)], 
        name="series4", background=background)

    db[constants.COL_SERIES].create_index([
        ("frequency", ASCENDING)], 
        name="series7", background=background)

    db[constants.COL_SERIES].create_index([
        ("start_ts", ASCENDING),        
        ("end_ts", ASCENDING)], 
        name="series8", background=background)

    db[constants.COL_TAGS].create_index([
        ("name", ASCENDING)], 
        name="name_idx", unique=True, background=background)

    db[constants.COL_TAGS].create_index([
        ("count", DESCENDING)], 
        name="count_idx", background=background)

    db[constants.COL_TAGS].create_index([
        ("count_datasets", DESCENDING)], 
        name="count_datasets_idx", 
        background=background,
        partialFilterExpression={"count_datasets": {"$exists": True}})

    db[constants.COL_TAGS].create_index([
        ("count_series", DESCENDING)], 
        name="count_series_idx", 
        background=background,
        partialFilterExpression={"count_series": {"$exists": True}})


print("Connect to first mongodb server...")
client_mongodb1 = MongoClient('mongodb1', 27018)
config = {
    '_id': 'widukind', 
    'members': [
        {'_id': 0, 'host': 'mongodb1:27018'}, 
        {'_id': 1, 'host': 'mongodb2:27018'}, 
        {'_id': 2, 'host': 'mongodb3:27018'}
    ]
}
client_mongodb1.admin.command("replSetInitiate", config)
print("Replicaset initialize: OK")

cpt = 0
max = 60
while True:
    print("Wait connect to replicaset...")
    cpt += 1
    if cpt > max:
        abort()
    try:
        mongodb1_replicaset = MongoClient('mongodb1', 27018, replicaset='widukind')
        mongodb1_replicaset.admin.command("replSetGetStatus")
        break
    except Exception as err:
        print("ERROR : ", str(err))
    time.sleep(1)
    print("wait...")

print("Connect to mongos router...")
try:
    router = MongoClient('mongorouter1', 27017)
    print("Add shard...")
    router.admin.command("addShard", "widukind/mongodb1:27018")
except Exception as err:
    print("ERROR : ", str(err))
    abort()

print("Create indexes...")
create_or_update_indexes(mongodb1_replicaset.widukind)

print("Configure sharding for widukind database...")
try:
    router.admin.command("enableSharding", "widukind")
    router.admin.command("shardCollection", "widukind.series", key={ "slug": 1 })
    router.admin.command("shardCollection", "widukind.datasets", key={ "slug": 1 })
    print("Configuration : OK")
except Exception as err:
    print("ERROR : ", str(err))
    abort()

print("End configuration.")

