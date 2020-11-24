import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DBHOST = os.getenv('DBHOST', '')
DBPORT = os.getenv('DBPORT', '')
DATABASE = os.getenv('DATABASE', '')
DBUSER = os.getenv('DBUSER', '')
DBPASSWORD = os.getenv('DBPASSWORD', '')


