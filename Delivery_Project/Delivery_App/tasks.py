# from dotenv import load_dotenv
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from datetime import datetime
import pytz
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')
CONNECTION_STRING = settings.CONNECTION_STRING
def db_connection():
    client = MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1)

    db = client['cartservice']
    col = db['orders']
    return client, col

def convert_objectid_to_string(data):  #convert mongodata into string
    """Recursively convert ObjectId to string in the dictionary."""
    if isinstance(data, dict):
        return {key: convert_objectid_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_string(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        # Convert datetime to ISO format string
        return data.isoformat() if data.tzinfo else data.replace(tzinfo=pytz.UTC).isoformat()
    return data

def Tasks_Section():
    try:
        client, col = db_connection()
        res = col.find({})
        orders_list = list(res)

        '''def convert_objectid_to_string(data):
            """Recursively convert ObjectId to string in the dictionary."""
            if isinstance(data, dict):
                return {key: convert_objectid_to_string(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_objectid_to_string(item) for item in data]
            elif isinstance(data, ObjectId):
                return str(data)
            elif isinstance(data, datetime):
                # Convert datetime to ISO format string
                return data.isoformat() if data.tzinfo else data.replace(tzinfo=pytz.UTC).isoformat()
            return data
    '''
        orders_list = convert_objectid_to_string(orders_list)
        return orders_list
    finally:
        client.close()

#download the orders from to end date
def task_list_daterange(from_date, end_date):
    try:
        client, col = db_connection()

        from_date = datetime.fromisoformat(from_date).replace(tzinfo=pytz.UTC)
        end_date = datetime.fromisoformat(end_date).replace(tzinfo=pytz.UTC)

        res = col.find({'$and': [{'createdAt': {'$gte': from_date}}, {'createdAt': {'$lte': end_date}}]})
        orders_list = list(res)

        '''def convert_mongo_data(data):
            """Recursively convert ObjectId and datetime to string in the dictionary."""
            if isinstance(data, dict):
                return {key: convert_mongo_data(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_mongo_data(item) for item in data]
            elif isinstance(data, ObjectId):
                return str(data)
            return data
    '''
        orders_list = convert_objectid_to_string(orders_list)
        return orders_list
        # logging.info(len(orders_list))
        # logging.info(orders_list)
    finally:
        client.close()



if __name__ == '__main__':
    # Tasks_Section()
    # task_list_daterange('2024-08-08T06:48:32.438+00:00', '2024-08-14T06:07:47.503+00:00')
    pass