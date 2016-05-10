#!/usr/bin/env python

"""
# Run this program
export COMPOSE_FILE=docker-compose-shard.yml
docker-compose run --rm --no-deps cli python /scripts/install_shard.py

# All remove
docker-compose down -v --rmi local
rm -rf mongodb redis

replSetInitiate
    ERROR :  already initialized <class 'pymongo.errors.OperationFailure'>

Add shard...
    ERROR :  E11000 duplicate key error collection: config.shards index: _id_ dup key: { : "widukind" } <class 'pymongo.errors.DuplicateKeyError'>

Configure sharding for widukind database...
    ERROR :  sharding already enabled for database widukind <class 'pymongo.errors.OperationFailure'>

"""

import sys
import time
import os

from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

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
        name="slug_idx", background=background)

    """
    db[constants.COL_PROVIDERS].create_index([
        ("name", ASCENDING)], 
        name="name_idx",
        unique=True,  
        background=background)
    """

    db[constants.COL_CATEGORIES].create_index([
        ("slug", ASCENDING)], 
        name="slug_idx", background=background)

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
        name="slug_idx", background=background)

    db[constants.COL_DATASETS].create_index([
        ("tags", ASCENDING)], 
        name="tags_idx", background=background)

    """    
    db[constants.COL_DATASETS].create_index([
        ('provider_name', ASCENDING), 
        ("dataset_code", ASCENDING)], 
        name="datasets1",
        unique=True,  
        background=background)
    """

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
        name="slug_idx", background=background)

    """
    db[constants.COL_SERIES].create_index([
        ("slug", pymongo.HASHED)], 
        background=background)
    """
    
    db[constants.COL_SERIES].create_index([
        ('provider_name', ASCENDING), 
        ("dataset_code", ASCENDING), 
        ("key", ASCENDING)
        ], 
        name="series1", 
        #unique=True, 
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

    """
    db[constants.COL_TAGS].create_index([
        ("name", ASCENDING)], 
        name="name_idx", unique=True, background=background)
    """

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

print("Replicaset initialize widukind1...")
try:
    client_mongodb1 = MongoClient('mongodb1', 27017)
    config = {
        '_id': 'widukind1', 
        'members': [
            {'_id': 0, 'host': 'mongodb1:27017'}, 
            {'_id': 1, 'host': 'mongodb2:27017'}, 
            {'_id': 2, 'host': 'mongodb3:27017'}
        ]
    }
    client_mongodb1.admin.command("replSetInitiate", config)
    print("Replicaset widukind1 initialized.")
except Exception as err:
    print("ERROR : ", str(err))
    abort()

print("Replicaset initialize widukind2...")
try:
    client_mongodb4 = MongoClient('mongodb4', 27017)
    config = {
        '_id': 'widukind2', 
        'members': [
            {'_id': 0, 'host': 'mongodb4:27017'}, 
            {'_id': 1, 'host': 'mongodb5:27017'}, 
            {'_id': 2, 'host': 'mongodb6:27017'}
        ]
    }
    client_mongodb4.admin.command("replSetInitiate", config)
    print("Replicaset widukind2 initialized.")
except Exception as err:
    print("ERROR : ", str(err))
    abort()

cpt = 0
max = 60
while True:
    print("Wait connect to replicasets...")
    cpt += 1
    if cpt > max:
        abort()
    try:
        mongodb1_replicaset = MongoClient('mongodb1', 27017, replicaset='widukind1')
        mongodb1_replicaset.admin.command("replSetGetStatus")
        
        mongodb4_replicaset = MongoClient('mongodb4', 27017, replicaset='widukind2')
        mongodb4_replicaset.admin.command("replSetGetStatus")
        
        break
    except Exception as err:
        print("ERROR : ", str(err))
    time.sleep(1)
    print("wait...")


print("Connect to first config server...")
try:
    client_mongoconfig1 = MongoClient('mongoconfig1', 27019)
    config = {
        '_id': 'configReplSet',
        'configsvr': True, 
        'members': [
            {'_id': 0, 'host': 'mongoconfig1:27019'}, 
            {'_id': 1, 'host': 'mongoconfig2:27019'}, 
            {'_id': 2, 'host': 'mongoconfig3:27019'}
        ]
    }
    client_mongoconfig1.admin.command("replSetInitiate", config)
    print("Replicaset for config servers initialize: OK")
except Exception as err:
    print("ERROR : ", str(err))
    abort()

print("Connect to mongos router...")
try:
    router = MongoClient('mongorouter1', 27017)
    print("Add shards...")
    router.admin.command("addShard", "widukind1/mongodb1:27017,mongodb2:27017,mongodb3:27017")
    router.admin.command("addShard", "widukind2/mongodb4:27017,mongodb5:27017,mongodb6:27017")
except Exception as err:
    print("ERROR : ", str(err))
    abort()

print("Configure sharding for widukind database...")
try:
    router.admin.command("enableSharding", "widukind")
    router.admin.command("shardCollection", "widukind.providers", key={ "name": 1 })
    #router.admin.command("shardCollection", "widukind.series", key={ "provider_name": 1, "dataset_code": 1, "key": 1 })
    router.admin.command("shardCollection", "widukind.series", key={ "slug": "hashed" }, unique=True) #numInitialChunks: 8192
    router.admin.command("shardCollection", "widukind.datasets", key={ "provider_name": 1, "dataset_code": 1 }, unique=True)
    print("Configuration : OK")
except Exception as err:
    print("ERROR : ", str(err))
    abort()

cpt = 0
max = 60
while True:
    print("Wait connect to mongodb...")
    cpt += 1
    if cpt > max:
        abort()
    try:
        client = MongoClient('mongorouter1', 27017)
        print("Create indexes...")
        create_or_update_indexes(client.widukind)
        break
    except Exception as err:
        print("ERROR : ", str(err))
    time.sleep(1)
    print("wait...")

print("End configuration.")

