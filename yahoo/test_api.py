'''
execute all tests in this file:
    >> python3 -m pytest test_api.py
test all in folder:
    >> python3 -m pytest
'''

import pytest
import os
from db import connection
from yahoo.api import Yahoo


COMPANY_NAME = 'ZUORA'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_yahoo_api():
    yahoo = Yahoo(connection=connection, output_folder=SCRIPT_DIR)
    res_success = yahoo.find_company_by_name(company_name=COMPANY_NAME)
    res_wrong = yahoo.find_company_by_name(company_name='___@_##')
    assert res_success['count'] > 0 , "The request was not successful. The data must be presents"
    assert res_wrong['count'] == 0, "The request was not successful. The data must not be presents"


