import os
from sqlalchemy import MetaData
metadata = MetaData()
from db.model.yahoo import yahoo_news, yahoo_historical
from sqlalchemy import create_engine
from config import DBHOST, DBPORT, DATABASE, DBUSER, DBPASSWORD

class Connection:
    def __init__(self, dbhost, dbport, database, dbuser, dbpassword, create_tables = True):
        self.__dbhost = dbhost
        self.__dbport = dbport
        self.__database = database
        self.__dbuser = dbuser
        self.__dbpassword =  dbpassword
        self.__engine = self.__db_connect()
        if create_tables:
            self.create_tables()

    def __get_connection_string(self):
        dbhost = self.__dbhost
        dbuser = self.__dbuser
        dbpassword = self.__dbpassword
        dbport = self.__dbport
        dbbase = self.__database
        return  f'mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbbase}'

    def __db_connect(self):
        return create_engine(self.__get_connection_string())

    def get_engine(self):
        return  self.__engine

    def get_connection(self):
        try:
            return self.__engine.connect()
        except:
            return None

    def create_tables(self):
        metadata.create_all(self.get_engine())

    def execute_sql(self, sql):
        rs = None
        with self.__engine.connect() as con:
            rs = con.execute(sql)
        return rs


connection = Connection(dbhost=DBHOST, dbport=DBPORT, database=DATABASE, dbuser=DBUSER, dbpassword=DBPASSWORD)