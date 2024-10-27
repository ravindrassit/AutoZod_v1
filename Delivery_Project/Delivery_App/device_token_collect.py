# from django.conf import settings
from pymongo import MongoClient
# CONNECTION_STRING = settings.CONNECTION_STRING
from bson.objectid import ObjectId

def get_device_token():
    with MongoClient('mongodb+srv://srk_cluster0:7N9u4iBRwA6BFOsK@cluster0.0dy4leu.mongodb.net/?retryWrites=true&w=majority' ,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['usermanagement']
        col = db['devicetokens']
        # device_token = col.find_one({"_id": '667694ae10bd37ffed161d7c'}, {'osToken.[0].token'})  # check this line carefully
        device_token = col.find_one({"_id": ObjectId('667694ae10bd37ffed161d7c')}, {'osToken.token':1, '_id': 0})  # check this line carefully
        # for item in device_token:
        #     print(item)
        print(device_token)
        print(device_token['osToken'][0]['token'])
get_device_token()