import os

from dotenv import load_dotenv
load_dotenv()
print(os.getenv('CONNECTION_STRING'))
print(os.getenv('DEBUG'))