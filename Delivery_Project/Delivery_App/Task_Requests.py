import os
import logging
# from dotenv import load_dotenv
from pymongo import MongoClient
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
from bson import ObjectId
from django.conf import settings

# load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')

def task_request():
    with MongoClient(settings.CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['cartservice']
        col = db['orders']
        res = col.find({},{'_id':1, 'status':1, 'updatedAt':1, 'dPartner':1, 'merchant.location.address':1, 'customer.location.address':1})
        final_res = (list(res))

        def convert_mongo_data(data):
            """Recursively convert ObjectId and datetime to string in the dictionary."""
            if isinstance(data, dict):
                return {key: convert_mongo_data(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_mongo_data(item) for item in data]
            elif isinstance(data, ObjectId):
                return str(data)
            return data

        final_res = convert_mongo_data(final_res)
        return final_res
        # logging.info(final_res)


if __name__ == '__main__':
    task_request()