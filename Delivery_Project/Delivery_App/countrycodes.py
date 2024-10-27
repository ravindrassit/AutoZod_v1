import logging
from pymongo import MongoClient
from django.conf import settings
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
from bson import ObjectId



CONNECTION_STRING = settings.CONNECTION_STRING

def country_codes():
    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['usermanagement']
        col = db['countrycodes']
        res = col.find({})

        def convert_mongo_data(data):
            """Recursively convert ObjectId and datetime to string in the dictionary."""
            if isinstance(data, dict):
                return {key: convert_mongo_data(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_mongo_data(item) for item in data]
            elif isinstance(data, ObjectId):
                return str(data)
            return data
        result = convert_mongo_data(list(res))
        return result

if __name__ == '__main__':
    result = country_codes()
    logger.info(result)
