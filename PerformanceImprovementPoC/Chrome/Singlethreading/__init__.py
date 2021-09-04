# !/usr/bin/env python
#!-*- coding: utf-8 -*-
# * for ChromeModel

import getpass
import os
import shutil
import database
from timeit import Timer
from statistics import mean

# version 2.1 test with chrome browser profile without treading
__version__ = "0.2.1"

# get windows user name
USERNAME = getpass.getuser()
# * chrome history
HISTORY = "History"

FILE_HANDLER = (
    "C:\\Users\\"
    + USERNAME
    + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"
    + HISTORY
)
TEST_DIR = (
    "C:\\Users\\"
    + USERNAME
    + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"
    + "SINGLETHREADING"
)
TEST_FILE = TEST_DIR + "\\History.sqlite"

# table name which is going to be requested
TABLE = "urls"
# def count_query() result - static test variable
ROW_COUNT = 4725 # 107
# first id in table - static test variable
START_ID = 1


def main():
    # ! Comment out for testing !
    # print(f"{FILE_HANDLER} _ target file")
    # if os.path.exists(TEST_DIR):
    #     print(f"{TEST_DIR} _ already exists!")
    # else:
    #     os.mkdir(TEST_DIR)
    #     print(f"{TEST_DIR} _ directory created!")
    # shutil.copy(FILE_HANDLER, TEST_FILE)
    # ! ----------------------- !

    dbms = database.MyDatabase(database.SQLITE, dbname="mydb.sqlite")

    def read_range(start, end):
        build = (
            "SELECT * FROM {TBL_HST} WHERE id BETWEEN "
            + str(start)
            + " AND "
            + str(end)
            + ";"
        )
        # print(build)
        query = build.format(TBL_HST=TABLE)
        dbms.print_all_data(query=query)

    def nonthreaded_testcase(iterations_i, result_list):
        for loop in range(iterations_i):
            # with threading module
            t = Timer(lambda: read_range(START_ID, ROW_COUNT))
            time = t.timeit(number=1)
            # print(f"Zeitmessung ohne Threading in ns - Durchlauf {loop + 1}: {time}")
            result_list.append(time)
        return result_list

    def show_results(iterations_i, result_list):
        # print("\n")
        # print(result_list)
        mean_value = mean(result_list)
        # plain_val = "%f" % mean_value
        # print(plain_val)
        print(f"Durchschnittswert über {iterations_i} Testläufe: {mean_value}\n")

    # important - deactivate test functions below line 93!
    # activate prints for count table and query content
    # in function def print_all_data in database.py
    #dbms.count_query()
    # activate prints for query content and more query content
    # in function def print_all_data in database.py
    #dbms.print_all_data(database.TABLE)

    #*Zeitmessung ohne Threading und Aufteilen der Lesezugriffe

    results_nonthreaded = []
    i = 800

    nonthreaded_testcase(i, results_nonthreaded)
    show_results(i, results_nonthreaded)


# run the program
if __name__ == "__main__":
    main()
