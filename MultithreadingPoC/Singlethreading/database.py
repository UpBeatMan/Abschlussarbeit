from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__version__ = "0.1.2"

# ! edit windows user name !
USERNAME = "Yochanan"
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
        # output switch
        # print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    # output switch
                    # print(row)
                    pass
                # print("\n")
                result.close()

    # Optional count query
    # def count_query(self):
    #     # sample query for testing
    #     # print("\n")
    #     query = "SELECT count(id) FROM {TBL_HST};".format(TBL_HST=TABLE)
    #     self.print_all_data(query=query)