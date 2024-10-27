import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


load_dotenv()
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
def create_new_team(data):
    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['adminportal'] #adddbname
        col = db['autoZodTeam'] #add collection name


        col.insert_one({'teamdetails': {'name': data['team_name']}})
        return 'resource created successfully'


def create_team_settings(data):
    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['cartservice']  # adddbname
        col = db['orders']  # add collection name

        col.insert_one({'team_name': data['team_name'], 'email': data['email']})
        return 'resource created successfully'



