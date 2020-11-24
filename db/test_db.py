'''
execute all tests in this file:
    >> python3 -m pytest test_db.py
test all in folder:
    >> python3 -m pytest
'''

import pytest
from db import Connection
from config import DBHOST, DBPORT, DATABASE, DBUSER, DBPASSWORD

def test_db_connection():
    connection_success = Connection(dbhost=DBHOST, dbport=DBPORT, database=DATABASE, dbuser=DBUSER,
                                    dbpassword=DBPASSWORD, create_tables=False).get_connection()
    connection_wrong = Connection(dbhost='localhost', dbport=3306, database='xyz', dbuser='xyz',
                                  dbpassword='xyz', create_tables=False).get_connection()
    assert connection_success is not None , "The request was not successful. Check credentials, database existence, etc"
    assert connection_wrong is  None, f"Connection with wrong credentials must be 'None'"


