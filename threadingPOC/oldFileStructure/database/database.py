from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oldFileStructure.database.tables import formhistory

__version__ = "0.1.1"

# database type
SQLITE = "sqlite"
# table names
HISTORY = "moz_formhistory"


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: "sqlite:///C:\\Users\\janwe\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\uvn3k0k7.dev-edition-default\\formhistory.sqlite"
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
            # session_create.configure()
            self.session = session_create()
        else:
            print("DBType is not found in DB_ENGINE")

    # Alternative Count
    def count_query(self):
        # sample query for testing
        # print("\n")
        query = "SELECT count(id) FROM {TBL_HST};".format(TBL_HST=HISTORY)
        self.print_all_data(query=query)

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

    # first try - not working yet!
    """What is dbms.get_count(q) -> see formhistory.py"""

    def count_all_rows(self, dbms):
        # rows = self.session.query(func.count(self.history.id)).scalar()
        # print(rows)
        history = formhistory
        # query from a class - test is not working
        q = self.session.query(history).fiter_by(id="1190").all()
        # # query using orm-enabled descriptors
        # q = self.session.query(history.id).all()
        print(dbms.get_count(q))
