import os
import logging
# from dotenv import load_dotenv
from pymongo import MongoClient
from django.conf import settings
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
from bson import ObjectId
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
import pytz
import json

# load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')

CONNECTION_STRING = settings.CONNECTION_STRING

def active_tasks_list(from_date, end_date):
    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['cartservice']
        col = db['orders']
        from_date = datetime.fromisoformat(from_date).replace(tzinfo=pytz.UTC)
        end_date = datetime.fromisoformat(end_date).replace(tzinfo=pytz.UTC)

        res = col.find({'$and': [{'createdAt': {'$gte': from_date}}, {'createdAt': {'$lte': end_date}}]})
        orders_list = list(res)

        def convert_mongo_data(data):
            """Recursively convert ObjectId and datetime to string in the dictionary."""
            if isinstance(data, dict):
                return {key: convert_mongo_data(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_mongo_data(item) for item in data]
            elif isinstance(data, ObjectId):
                return str(data)
            return data

        orders_list = convert_mongo_data(orders_list)
        return orders_list
        # logging.info(len(orders_list))
        # logging.info(orders_list)


def dashboard_map(merchant_id):
    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['adminportal']
        col = db['merchants']

        # # Sample string ID
        # string_id = "66374e52ea7ffba3c7deed7c"
        #
        # # Convert string to ObjectId
        # object_id = ObjectId(string_id)

        object_id = ObjectId(merchant_id)

        # res = col.find({'profile.roles.name': 'Merchant'}, {'location': 1})
        # res = col.find_one({'_id':'}, {'geoPoint.coordinates': 1})
        res = col.find_one({'_id': object_id},{'profile.firstName':1, 'profile.lastName':1, 'email':1, 'geoPoint.coordinates':1})
        result = res
        # logging.info(result)
        def convert_mongo_data(data):
            """Recursively convert ObjectId and datetime to string in the dictionary."""
            if isinstance(data, dict):
                return {key: convert_mongo_data(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_mongo_data(item) for item in data]
            elif isinstance(data, ObjectId):
                return str(data)
            return data

        result = convert_mongo_data(result)
        return result

def dashboard_agent_list():
    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['usermanagement']
        col = db['deliverypersons']
        total_delivery_persons = list(col.find({}))
        def convert_mongo_data(data):
            """Recursively convert ObjectId and datetime to string in the dictionary."""
            if isinstance(data, dict):
                return {key: convert_mongo_data(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_mongo_data(item) for item in data]
            elif isinstance(data, ObjectId):
                return str(data)
            return data

        total_delivery_persons = convert_mongo_data(total_delivery_persons)


        return total_delivery_persons
        # logging.info(len(total_delivery_persons))
        # logging.info(total_delivery_persons)


if __name__ == '__main__':
    # active_tasks_list('2024-08-08T06:48:32.438+00:00', '2024-08-14T06:07:47.503+00:00')
    # dashboard_map('65a37ea8380d4ea0e51bbab0')
    # dashboard_agent_list()
    pass