import requests
import logging
import orders
import os
from dotenv import load_dotenv
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
    db = client['cartservice']
    col = db['orders']

def automate_order_assignment_deliveryperson(payload, url ):
    response = requests.post(url=url, data=payload)
    if response.status_code == 201:
        # logger.info(f'order successfully assigned to nearest delivery person.')
        col.updateOne({"_id":payload["order_id"]},{"$set":{"status":" "}}) #need to update the status

    else:
        logger.error(f"Failed to assign order to delivery person.")


