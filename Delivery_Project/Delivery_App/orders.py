import threading
import queue
# import time
import logging
# import geopy.distance
# from datetime import datetime
import os
# from dotenv import load_dotenv
from django.conf import settings
from .delivery_person1 import delivery_action

from pymongo import MongoClient

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')
CONNECTION_STRING = settings.CONNECTION_STRING

def orders_action():
    # client = MongoClient('mongodb+srv://srk_cluster0:7N9u4iBRwA6BFOsK@cluster0.0dy4leu.mongodb.net/?retryWrites=true&w=majority',
    #                      maxPoolSize=10,maxIdleTimeMS=3000,maxConnecting=1)

    # with MongoClient('mongodb+srv://srk_cluster0:7N9u4iBRwA6BFOsK@cluster0.0dy4leu.mongodb.net/?retryWrites=true&w=majority',
    #     maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['cartservice']
        col = db['orders']

        '''res = col.find({'$or':
        [
            {"paymentMode": "COD", "status": {'$nin': ["PayFailed", "Completed", "Cancelled","Delivered"]}},
            {"paymentMode": {'$ne': "COD"}, "status": {'$nin': ["Pending", "PayFailed", "Completed", "Cancelled", "Delivered"]}}
        ],"dPartner.name": " "}
        ) #.sort({"createdAt":1})
        '''
        res = col.find(
            {
                '$and': [
                    {
                        '$or': [
                            {"paymentMode": "COD",
                             "status": {'$nin': ["PayFailed", "Completed", "Cancelled", "Delivered"]}},
                            {"paymentMode": {'$ne': "COD"},
                             "status": {'$nin': ["Pending", "PayFailed", "Completed", "Cancelled", "Delivered"]}}
                        ]
                    },
                    {
                        '$or': [
                            {"dPartner.name": ""},
                            {"dPartner.name": {"$exists": False}}
                        ]
                    }
                ]
            }
        )

        # print(f'total records are:{len(list(res))}')

        merchants_id =[]
        unique_merchants_id = []
        merchants_name = []
        unique_merchants_name = []


        # sorting the objects based on the orders created date
        sorted_list_by_createdAt = sorted(res, key=lambda x: x['createdAt'])
        logger.info(f'length is:{len(sorted_list_by_createdAt)}')
        logger.info(f'sorting list by datetime:{sorted_list_by_createdAt}')



        # implement queue terminology for orders
        max_queue_length = 10 #eval(input('enter your queue length:'))
        # max_queue_length = int(orders) #eval(input('enter your queue length:'))
        # min_queue_length = 3
        queue = []
        for item in sorted_list_by_createdAt:
            if len(queue) < max_queue_length:  #(0,1),(1,2),(2,3),(3,4),(4,fail)
                queue.append(item)
            elif len(queue) >= max_queue_length:
                # print(f'queue is full')
                logger.info(f'queue full')
                break
            else:
                pass

        logger.info(f'length:{len(queue)}, queue is:{queue}')

        d = {}

        for records in sorted_list_by_createdAt:
            # print(records)
            merchants_id.append(records['merchant']['id'])
            distance = (records['merchant']['location']['latitude'],records['merchant']['location']['longitude'])
            merchants_name.append(records['merchant']['name'])
            # print(f"latitude:{distance['latitude']},longitude:{distance['longitude']}")

            if records['merchant']['id'] not in d:
                merchantID = records['merchant']['id']
                d[merchantID] = [records['merchant']['name'],distance]
                # d['merchant_location'] = distance

        for item in merchants_id:
            if item not in unique_merchants_id:
                unique_merchants_id.append(item)
        # unique_merchants_id = list(set(merchants_id))


        for item in merchants_name:
            if item not in unique_merchants_name:
                unique_merchants_name.append(item)

    return merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue


# while True:
#     thread = threading.Thread(target=orders_action, args=(,))
#     thread.start()
#     time.sleep(5)


master_result = []

'''def run_function():
    thread = threading.Timer(60.0, run_function)
    thread.start()
    result = orders_action()
    # master_result.append(result)
    return result
'''

def run_function():

    thread = threading.Timer(120.0, run_function)
    thread.start()
    result = orders_action()  #result object store the result in tuple format
    result = list(result).pop(5) #length of result object is 6, so removed last indexed item and store return result into result object.
    print(f'result is:{result}')
    # master_result.extend(result)
    master_result = result


    if len(master_result) > 0:
        queue = master_result
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(len(queue))
        # thread = threading.Thread(target=delivery_action, args=(queue,))
        # thread.start()

        result = delivery_action(queue)
        return result

    # return result


if __name__ == '__main__':

    #merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue = orders_action(3)
    # merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue = run_function()
    # print(d)
    #logger.info(f'merchantid:{merchants_id}')
    # print(f'unique_merchant_id:{unique_merchants_id}')
    #logger.info(f'merchants_name:{merchants_name}')
    # print(f'unique_merchants_name:{unique_merchants_name}')

    run_function()

