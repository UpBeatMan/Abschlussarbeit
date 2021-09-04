# !/usr/bin/env python
#!-*- coding: utf-8 -*-
# * for ChromeModel

import getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# database module version 2.3 with getpass and for chrome data structure
__version__ = "0.2.3"

# get windows user name
USERNAME = getpass.getuser()
# * database type
SQLITE = "sqlite"
# * chrome history
HISTORY = "History"
TABLE = "urls"


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: SQLITE + ":///C:\\Users\\"
        + USERNAME
        + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\SINGLETHREADING\\"
        + HISTORY + "." + SQLITE
    }
    # main db connection reference object
    db_engine = None

    def __init__(self, dbtype, username="", password="", dbname=""):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            # print(self.db_engine)
            session_create = sessionmaker(bind=self.db_engine)
            self.session = session_create()
        else:
            print("DBType is not found in DB_ENGINE")

    # show all data from table
    def print_all_data(self, table="", query=""):
        query = query if query != "" else "SELECT * FROM '{}';".format(table)
        # output switch - count table
        #print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    # output switch - query content
                    #print(row)
                    pass
                # output switch - more query content
                #print("\n")
                result.close()

    # Optional count query - activate in singlethreading.py
    def count_query(self):
        # sample query for testing
        query = "SELECT count(id) FROM {TBL_HST};".format(TBL_HST=TABLE)
        self.print_all_data(query=query)
