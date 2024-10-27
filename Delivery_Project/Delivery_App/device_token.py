import logging
from pymongo import MongoClient
# from django.conf import settings
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
from bson import ObjectId


# CONNECTION_STRING = settings.CONNECTION_STRING

# def device_token_collect(partnerId):
partnerId = '667694ae10bd37ffed161d7c'
def device_token_collect(partnerId):
    with MongoClient("mongodb+srv://srk_cluster0:7N9u4iBRwA6BFOsK@cluster0.0dy4leu.mongodb.net/?retryWrites=true&w=majority", maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['usermanagement']
        col = db['devicetokens']
        device_token_result = col.find_one({"_id": ObjectId(partnerId)},
                                           {'osToken.token': 1, '_id': 0})  # check this line carefully
        print(device_token_result)
        device_token = device_token_result['osToken'][0]['token']
        print(device_token)


device_token_collect(partnerId)