import logging

from pymongo import MongoClient
from django.conf import settings
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
from bson import ObjectId
from pymongo.errors import ConnectionFailure

# load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')
CONNECTION_STRING = settings.CONNECTION_STRING





def AutoZodSettings(data):
    with MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=3000, maxConnecting=1) as client:
        db = client['adminportal']
        col = db['autozodSettings']
        #general settings
        time_zone = data['time_zone']
        team_logo = data['team_logo']

        #task settings
        task_assign_mode = data['task_assign_mode']
        max_tasks_per_agent = data['max_tasks_per_agent']
        task_lock_minutes = data['task_lock_minutes']
        agent_task_accept_seconds = data['agent_task_accept_seconds']

        #auto assign settings
        auto_assign_mode = data['auto_assign_mode']
        auto_assign_retries = data['auto_assign_retries']
        auto_assign_retry_backoff = data['auto_assign_retry_backoff']
        task_agent_max_radius = data['task_agent_max_radius']  #radius

        #route settings

        #api settings

        #language rules

        #distance and time settings ##not now

        #map settings

        #agent commission settings
        commission_calculation = data['commission_calculation']
        commission_logic = data['commission_logic']

        #distance time commission settings
        minimum_wage = data['minimum_wage']
        distance_based_incentive_rules = data['distance_based_incentive_rules']
        time_based_incentive_rules = data['time_based_incentive_rules']


        #language client settings

        res = col.insert_one({'general_settings':
                                  {'time_zone': time_zone, 'team_logo': team_logo},
                              'task_settings':{'task_assign_mode': task_assign_mode, 'max_tasks_per_agent': max_tasks_per_agent,'task_lock_minutes': task_lock_minutes, 'agent_task_accept_seconds': agent_task_accept_seconds},
                              'auto_assign_settings':{'auto_assign_mode': auto_assign_mode, 'auto_assign_retries': auto_assign_retries, 'auto_assign_retry_backoff': auto_assign_retry_backoff,'task_agent_max_radius': task_agent_max_radius},
                              'agent_commission_settings':{'commission_calculatio': commission_calculation,'commission_logic': commission_logic},
                              'distance_time_commission_settings':{'minimum_wage': minimum_wage,'distance_based_incentive_rules': distance_based_incentive_rules, 'time_based_incentive_rules': time_based_incentive_rules}
                              })
        logger.info('resource created successfully')
        return 'resource created successfully'

if __name__ == '__main__':
    # AutoZodSettings()
    pass

