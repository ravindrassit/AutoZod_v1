'''from pymongo import MongoClient
from .orders import orders_action, run_function
import geopy.distance
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue  = orders_action()
# merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue  = run_function()

load_dotenv()
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
def delivery_action(orders):
    merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue = orders_action(orders)
    # merchants_id, unique_merchants_id, merchants_name, unique_merchants_name, d, queue  = run_function()

    # client = MongoClient('mongodb+srv://srk_cluster0:7N9u4iBRwA6BFOsK@cluster0.0dy4leu.mongodb.net/?retryWrites=true&w=majority',
    #                      maxPoolSize=10,maxIdleTimeMS=3000,maxConnecting=1)

    with MongoClient(CONNECTION_STRING,maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:

        db = client['usermanagement']
        col = db['deliverypersons']
        query = {'activityStatus':'Online'}

        total_records = col.find(query)

    #filter records based on the merchant_id and activitystatus has online and return total delivery persons list for corresponding merchant

        lst1 = []  #delivery persons sorting list
        for item in queue:
            merchant_id = item['merchant']['id']
            merchant_name = item['merchant']['name']
            logger.info(f'merchantid:{merchant_id}')
            merchant_location = (item['merchant']['location']['latitude'], item['merchant']['location']['longitude'])
            list_object = col.find({'$and':[{'activityStatus':'Online'},{'adminID':merchant_id}]})
            logger.info(f'list object:{list_object}')
            delivery_person_list = list(list_object)
            # for item in delivery_person_list:
            #     print(item)
            logger.info(f'total delivery persons: {len(delivery_person_list)}')

            # merchant_delivery_distance = {}
            # sorted_list={}

            #sort the delivery person locations by comparing the merchant location and delivery person location
            def display(merchant_location, delivery_person_list):
                merchant_delivery_distance = {}
                for item in delivery_person_list:
                    if 'clat' in item and 'clon' in item:
                        delivery_location = (item['clat'],item['clon'])
                        logger.info(f'distance:{geopy.distance.geodesic(merchant_location, delivery_location).km}')
                        distance = geopy.distance.geodesic(merchant_location, delivery_location).km
                        merchant_delivery_distance[distance] = item

                logger.info(f'res is:{merchant_delivery_distance}')
                logger.info(f'length of reasult is:{len(merchant_delivery_distance)}')
                sorted_list = dict(sorted(merchant_delivery_distance.items()))
                lst1.append(sorted_list)
                # sorted_list = sorted_list
                logger.info(f'sorting the merchant_delivery_distance: {sorted_list}')
            display(merchant_location,delivery_person_list )

        #iterate the sorted list of delivery persons who are matched with the corresponding merchat_id

        lst =[] #this object contains the each order merchant name and delivery person name
        # print(f'lst is:{lst1}')
        # print('+++++++++++++++')
        # print(f'length:{len(lst1)}')
        for item in lst1:
            for key, value in item.items():
                # print(key,value)
                d={} #current order merchant name and delivery person name store

                if value['activityStatus'] == 'Offline':
                    logger.info(f'delivery person status is offline')
                elif value['activityStatus'] == 'Online':  #Online
                    # print(f'order is assign to current delivery person and person name is:{value["firstName"]}')
                    d['merchant_name']=merchant_name
                    d['deliver_name'] = value["firstName"]
                    lst.append(d)
                    # return f'{{"merchant": "{merchant_name}", "deliver_name": "{value["firstName"]}"}}'
                    #del queue[item]  #this line is delete the active order from queue once the order assign complete
                    break      #exit the loop as soon as activitystatus found online
                elif value['activityStatus'] == 'busy':
                    logger.info(f'delivery person busy with other order to delivery the order to customer')

                else:
                    logger.info(f'available delivery person not found so still searching')
        logger.info(f'final:{lst}')
    return lst


#delivery_action()
    # break
'''






