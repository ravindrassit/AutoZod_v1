import json

from pymongo import MongoClient
from django.conf import settings
# from .orders import orders_action, run_function
# from .auto_assignment import automate_order_assignment_deliveryperson
import geopy.distance
import logging
# from dotenv import load_dotenv
import os
import requests
import copy
from bson.objectid import ObjectId

from .fcm_token_generate import fcm_token

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue  = orders_action()
# merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue  = run_function()

# load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')
CONNECTION_STRING = settings.CONNECTION_STRING
Notification_Duration = settings.NOTIFICATION_DURATION

def delivery_action(queue):

    #merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue = orders_action(orders)
    # merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue  = run_function()

    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['usermanagement']
        col = db['deliverypersons']
        query = {'activityStatus':'Online'}

        total_records = col.find(query)

        orders_list = list()
        logger.info(f'initially the lst object length is:{len(orders_list)}')

        # filter records based on the merchant_id and activitystatus has online and return total delivery persons list for corresponding merchant
        for item in queue:
            # order_object_id = item['_id']
            order_id = str(item['_id'])  # convert order id from object type to string type
            adminId = item['adminId']
            merchant_id = item['merchant']['id']
            merchant_name = item['merchant']['name']
            logger.info(f'merchantid:{merchant_id}')
            merchant_location = (item['merchant']['location']['latitude'], item['merchant']['location']['longitude'])
            # list_object = col.find({'$and':[{'activityStatus':'Online'},{'adminID':merchant_id}]})
            list_object = col.find({'$and':[{'activityStatus':'Online'},{'adminID':adminId}]})
            logger.info(f'list object:{list_object}')
            delivery_person_list = list(list_object)
            # for item in delivery_person_list:
            #     print(item)
            logger.info(f'total delivery persons: {len(delivery_person_list)}')

            # merchant_delivery_distance = {}
            # sorted_list={}

            #sort the delivery person locations by comparing the merchant location and delivery person location
            lst1 = []  #delivery persons sorting list
            def display(merchant_location, delivery_person_list):
                merchant_delivery_distance = {}
                for item in delivery_person_list:
                    if 'clat' in item and 'clon' in item:
                        delivery_location = (item['clat'],item['clon'])
                        logger.info(f'distance:{geopy.distance.geodesic(merchant_location, delivery_location).km}')
                        distance = geopy.distance.geodesic(merchant_location, delivery_location).km
                        merchant_delivery_distance[distance] = item

                logger.info(f'res is:{merchant_delivery_distance}')
                logger.info(f'after comparing the distance between merchant and delivery person length of result is:{len(merchant_delivery_distance)}')
                sorted_list = dict(sorted(merchant_delivery_distance.items()))
                lst1.append(sorted_list)
                logger.info(f'sorting the merchant_delivery_distance: {sorted_list}')
            display(merchant_location,delivery_person_list )

            #iterate the sorted list of delivery persons who are matched with the corresponding merchat_id
            for obj in lst1:
                for key, value in obj.items():
                    # print(key,value)
                    # d={}

                    if value['activityStatus'] == 'Offline':
                        logger.info(f'delivery person status is offline')
                    elif value['activityStatus'] == 'Online':  #Online
                        # d['order_id'] = order_id
                        # d['merchant_name'] = merchant_name
                        # d['deliver_name'] = value["firstName"]+' '+value["lastName"]
                        # orders_list.append(d)
                        orders_list.append({'order_id':order_id,'adminId':str(adminId),'merchant_name':merchant_name,'deliver_name':value["firstName"]+' '+value["lastName"],'partnerId':str(value['_id'])})



                        #this code of lines write for orders assign delivery persons automatically by passing order_Id and partner_Id details as apayload.

                        '''def automate_order_assignment_deliveryperson(payload, url):
                            response = requests.post(url=url, json=payload,headers={"Content-Type": "application/json"})
                            logger.info(f'initial response:{response}')
                            logger.info(f'response is:{response.json()},status code is:{response.status_code}')
                            if response.status_code == 200:
                                logger.info(f'order successfully assigned to nearest delivery person.')
                                # col.updateOne({"_id": order_object_id},
                                #               {"$set": {"status": "assigned"}})  # need to update the status like assigned

                            else:
                                logger.error(f"Failed to assign order to delivery person.")

                        payload = {"orderId":order_id,"partnerId":str(value['_id'])}
                        logger.info(f'payload is:{payload}')
                        automate_order_assignment_deliveryperson(payload, url = "https://zhzmlspf-8080.inc1.devtunnels.ms/api/admin/orders/assign")
                        '''


                        # def automate_order_assignment_deliveryperson(payload, url):
                        '''def automate_order_assignment_deliveryperson():

                            #accept/decline notifications
                            # order_id = payload['orderId']
                            partnerId = value["_id"]
                            with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

                                db = client['usermanagement']
                                col = db['devicetokens']
                                device_token_result = col.find_one({"_id": ObjectId(partnerId)},{'osToken.token':1, '_id':0}) #check this line carefully
                                # device_token = device_token_result['osToken'][0]['token']
                                if device_token_result is not None:
                                    device_token = device_token_result['osToken'][0]['token']
                                    if device_token is not None:
                                        notification_payload = {
                                            "message": {
                                                "token": device_token,
                                                "data": {
                                                    "id": "102",
                                                    "title": "New Order Request",
                                                    "body": "At Panjagutta",
                                                    "sound": "bell",
                                                    "is_ride": "true",
                                                    "duration": "60000"
                                                },
                                                "android": {
                                                    "priority": "HIGH"
                                                }
                                            }
                                        }
                                        #add notification time limit 60 seconds
                                        token = fcm_token() #fcm token store in result variable
                                        response = requests.post(url='https://fcm.googleapis.com/v1/projects/zaperr-288b8/messages:send', json=notification_payload, headers={"Authorization": f'Bearer {token}', "Content-Type": "application/json"})
                                        logger.info(f'fcm token response: {response.json()}')
                                        data = response.json()
                                        if data['notification_status'] == 'accept':
                                            payload = {"orderId": data['orderId'], "partnerId": data['dpartnerId']}
                                        ###########
                                        if response == 'accept':
                                   
                                            response = requests.post(url=url, json=payload,headers={"Content-Type": "application/json"})
                                
                                            if response.status_code == 200:
                                                logger.info(f'order successfully assigned to nearest delivery person.')
                                                break                               
                                    
                                            else:
                                                logger.error(f"Failed to assign order to delivery person.")
                                                
                                        elif data['notification_status'] == 'decline':
                                            logger.info(f'you are decline the order')
                                            #continue
                                            notification_payload = {    
                                                "message": {
                                                    "token": device_token,
                                                    "data": {
                                                        "id": order_id,
                                                        "title": "",
                                                        "body": "",
                                                        "sound": "bell",
                                                        # "is_cancelled": "false",
                                                        "is_ride": "false",
                                                        "duration": "60000"
                                                    },
                                                    "android": {
                                                        "priority": "HIGH"
                                                    }
                                                }
                                            }
                                            response = requests.post(url='https://fcm.googleapis.com/v1/projects/zaperr-288b8/messages:send', json=notification_payload, headers={"Authorization": token, "Content-Type": "application/json"})
                                        
                                        #######


                        # payload = {"orderId":order_id,"partnerId":str(value['_id'])}
                        # logger.info(f'payload is:{payload}')
                        # automate_order_assignment_deliveryperson(payload, url = "https://zhzmlspf-8080.inc1.devtunnels.ms/api/admin/orders/assign")
                        automate_order_assignment_deliveryperson()
                        '''






                        # del queue[item]  #this line is delete the active order from queue once the order assign complete
                        break      #exit the loop once the current order assign to nearest delivery person.
                    elif value['activityStatus'] == 'busy':
                        logger.info(f'delivery person busy with other order to delivery the order to customer')

                    else:
                        logger.info(f'available delivery person not found so still searching')

            #forcefully order assign to first delivery person if no one accept order
            '''else:
                first_delivery_person_details = lst1[0]
                for key, value in first_delivery_person_details.items():
                    order_id = order_id
                    merchant_name = merchant_name
                    deliver_name = value["firstName"]+' '+value["lastName"]
                    partnerId = str(value['_id'])
                    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

                        db = client['usermanagement']
                        col = db['devicetokens']
                        device_token_result = col.find_one({"_id": ObjectId(partnerId)},
                                                           {'osToken.token': 1, '_id': 0})  # check this line carefully
                        # device_token = device_token_result['osToken'][0]['token']
                        if device_token_result is not None:
                            device_token = device_token_result['osToken'][0]['token']
                            if device_token is not None:
                                notification_payload = {
                                    "message": {
                                        "token": device_token,
                                        "data": {
                                            "id": "102",
                                            "title": "Order Assigned",
                                            "body": "New order has been assigned to you",
                                            "sound": "audiomass",
                                            "is_assign": "true",
                                            "duration": "60000"
                                        },
                                        "android": {
                                            "priority": "HIGH"
                                        }
                                    }

                                }
                                token = fcm_token()  # fcm token store in result variable
                                response = requests.post(
                                    url='https://fcm.googleapis.com/v1/projects/zaperr-288b8/messages:send',
                                    json=notification_payload,
                                    headers={"Authorization": f'Bearer {token}', "Content-Type": "application/json"})
                                logger.info(f'fcm token response: {response.json()}')
                                payload = {"orderId":order_id,"partnerId":str(value['_id'])}
                                requests.post(url = 'https://zhzmlspf-8080.inc1.devtunnels.ms/api/admin/orders/assign', json = payload, headers={"Content-Type": "application/json"})
            #forcefully order assign code end here.
            '''


        logger.info(f'final:{orders_list}')
        logger.info(f'after 10 records the length of lst object is:{len(orders_list)}')
        final_list = orders_list.copy()
        del orders_list
        logger.info(f'final list:{final_list}')
        logger.info(f'the length of final list object is:{len(final_list)}')
    return final_list


#delivery_action()
    # break







