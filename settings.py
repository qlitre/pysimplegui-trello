import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TRELLO_USER_ID = os.environ.get('TRELLO_USER_ID')
TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_API_SECRET = os.environ.get('TRELLO_API_SECRET')
TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')
