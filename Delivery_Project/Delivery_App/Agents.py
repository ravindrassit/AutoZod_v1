import os
import logging
# from dotenv import load_dotenv
from pymongo import MongoClient
from django.conf import settings
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
from bson import ObjectId
from pymongo.errors import ConnectionFailure

# load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')
CONNECTION_STRING = settings.CONNECTION_STRING

'''def Agent():
    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['usermanagement']
        col = db['deliverypersons']

        # db = client['adminportal']
        # col = db['merchants']
        res = col.find({},{'_id':0,'firstName':1, 'lastName':1, 'email':1, 'phone':1})
        result = list(res)
        # logging.info(len(result))
        # logging.info(result)
        return result

def Agent_display(phone):
    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['usermanagement']
        col = db['deliverypersons']


        res = col.find_one({'phone':phone})
        result = res
        # logging.info(len(result))
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

        orders_list = convert_mongo_data(result)
        return orders_list



def Agent_update(phone, data):
    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['usermanagement']
        col = db['deliverypersons']

        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email']
        phone = data['phone']

        col.update_one({'phone':phone},{'$set':{'firstName':firstName, 'lastName':lastName, 'email':email, 'phone':phone }})
        # result = list(res)
        # logging.info(len(result))
        # logging.info(result)
        return f'details updated successfully'


def Agent_delete(phone):
    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['usermanagement']
        col = db['deliverypersons']

        col.delete_one({'phone':phone})
        return 'details deleted successfully'

def Agent_create(data):
    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['usermanagement']
        col = db['deliverypersons']
        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email']
        phone = data['phone']
        col.insert_one({'firstName': firstName, 'lastName': lastName, 'email': email, 'phone': phone})
        # return 'resource created successfully'
        logging.info('resource created successfully')


if __name__ == '__main__':
    # Agent()
    # Agent_display(email = 'jhada@hjhjd.com')
    Agent_create(data={'firstName': 'ravindra', 'lastName': 'reddy', 'email': 'Ravindra.S@silversnakeit.com', 'phone': '7204273233'})
    # pass
'''

'''client = MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1)
db = client['usermanagement']
col = db['deliverypersons']

def Agent():

    res = col.find({},{'_id':0,'firstName':1, 'lastName':1, 'email':1, 'phone':1})
    result = list(res)
    # logging.info(len(result))
    # logging.info(result)
    return result

def Agent_display(phone):

    res = col.find_one({'phone':phone})
    result = res
    # logging.info(len(result))
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

    orders_list = convert_mongo_data(result)
    return orders_list



def Agent_update(phone, data):

    firstName = data['firstName']
    lastName = data['lastName']
    email = data['email']
    phone = data['phone']

    col.update_one({'phone':phone},{'$set':{'firstName':firstName, 'lastName':lastName, 'email':email, 'phone':phone }})
    # result = list(res)
    # logging.info(len(result))
    # logging.info(result)
    return f'details updated successfully'


def Agent_delete(phone):

    col.delete_one({'phone':phone})
    return 'details deleted successfully'

def Agent_create(data):
   
        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email']
        phone = data['phone']
        col.insert_one({'firstName': firstName, 'lastName': lastName, 'email': email, 'phone': phone})
        return 'resource created successfully'
        # logging.info('resource created successfully')

# client.close() #Exception Value:	Cannot use MongoClient after close (if we close the db connection then raise this eror.)


if __name__ == '__main__':
    # Agent()
    # Agent_display(email = 'jhada@hjhjd.com')
    # Agent_create(data={'firstName': 'ravindra', 'lastName': 'reddy', 'email': 'Ravindra.S@silversnakeit.com', 'phone': '7204273233'})
    pass
'''

def db_connection():
    client = MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1)
    db = client['usermanagement']
    col = db['deliverypersons']
    return client, col

def Agent():
    client, col =None, None
    try:
        client, col = db_connection()
        res = col.find({},{'_id':0,'firstName':1, 'lastName':1, 'email':1, 'phone':1, 'activityStatus':1,'accountStatus':1})
        result = list(res)
        # logging.info(len(result))
        # logging.info(result)
        return result
    except Exception as e:
        return []
    finally:
        if client:
            client.close()

def Agent_display(phone):
    client, col = None, None
    try:
        client, col = db_connection()
        res = col.find_one({'phone':phone})
        result = res
        # logging.info(len(result))
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

        orders_list = convert_mongo_data(result)
        return orders_list
    except Exception as e:
        return []
    finally:
        if client:
            client.close()


def Agent_update(phone, data):
    client, col = None, None
    try:
        client, col = db_connection()

        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email']
        phone = data['phone']

        col.update_one({'phone':phone},{'$set':{'firstName':firstName, 'lastName':lastName, 'email':email, 'phone':phone }})
        # result = list(res)
        # logging.info(len(result))
        # logging.info(result)
        return f'details updated successfully'
    except Exception as e:
        return []
    finally:
        if client:
            client.close()

def Agent_delete(phone):
    client, col = None, None
    try:
        client, col = db_connection()

        col.delete_one({'phone':phone})
        return 'details deleted successfully'
    except Exception as e:
        return []
    finally:
        if client:
            client.close()
def Agent_create(data):
    client, col = None, None
    try:
        client, col = db_connection()
        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email']
        activityStatus = data['activityStatus']
        accountStatus = data['accountStatus']
        countryCode = data['countryCode']
        phone = data['phone']
        gender = data['gender']
        dateOfBirth = data['dateOfBirth']
        #adminId nothing but merchantId, here assign Desikitchen merchantId statically
        col.insert_one({'adminID': ObjectId('66580f59c49d13ddc3ed36c1'), 'username': '', 'password': '', 'email': email, 'countryCode': countryCode, 'phone': phone,
                        'inviterID': '', 'inviteCode': {'code': '', 'expiration': 0},
                        'tags': None,'firstName': firstName,'lastName': lastName,'dateOfBirth': dateOfBirth,'gender': gender,'lastLogin': '0001-01-01T00:00:00.000+00:00',
                        'twoFactorAuthentication': {'enabled': False, 'secretKey': '', 'verificationStatus': False},
                        'accountVerification': {'status': '', 'token': ''}, 'activityStatus': activityStatus, 'accountStatus': accountStatus, 'ratings': None,
                        'geoPoint':{'type': 'Point','coordinates':[1,2] },'createdAt': '', 'updatedAt':'','profilePic': '',})


        return 'resource created successfully'
        # logging.info('resource created successfully')
    # except Exception as e:
    #     return 'resource not created successfully'
    finally:
        if client:
            client.close()



def agent_action(data):
    client, col = None, None
    try:
        client, col = db_connection()
        activityStatus = data['actions']
        accountStatus = data['accountStatus']
        phone = data['phone']
        if activityStatus == 'enable':
            col.update_one({'phone': phone},
                           # {'$set': {'accountStatus': accountStatus, 'activityStatus': activityStatus}})
                           {'$set': {'accountStatus': accountStatus, 'activityStatus': 'online'}})
            return 'resource updated successfully'
        elif activityStatus == 'disable':
            col.update_one({'phone': phone},{'$set': {'accountStatus': accountStatus, 'activityStatus': 'offline'}})
            return 'resource updated successfully'

    finally:
        if client:
            client.close()

if __name__ == '__main__':
    # Agent()
    # Agent_display(email = 'jhada@hjhjd.com')
    # Agent_create(data={'firstName': 'ravindra', 'lastName': 'reddy', 'email': 'Ravindra.S@silversnakeit.com', 'phone': '7204273233'})
    pass