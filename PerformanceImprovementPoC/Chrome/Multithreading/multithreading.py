# !/usr/bin/env python
#!-*- coding: utf-8 -*-
# * for ChromeModel

import getpass
import os
import shutil
import database
from threading import Thread
from timeit import Timer
from statistics import mean

# version 2.2 test with chrome browser profile with threading
__version__ = "0.2.2"

# * choose thread count
TH_LOW: int = 2
TH_MED: int = 4
TH_HIG: int = 8

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
    + "MULTITHREADING"
)
TEST_FILE = TEST_DIR + "\\History.sqlite"

# table name which is going to be requested
TABLE = "urls"
# def count_query() result - static test variable
ROW_COUNT = 107 # 4725
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

    def threaded_testcase(iterations_i, result_list, threads):
        for loop in range(iterations_i):
            # with threading module
            t = Timer(lambda: calc_borders(START_ID, ROW_COUNT, threads))
            time = t.timeit(number=1)
            # print(
            #     f"Zeitmessung mit {threads} Threads in ns - Durchlauf {loop + 1}: {time}"
            # )
            result_list.append(time)
        return result_list

    def show_results(iterations_i, result_list, threads):
        # print("\n")
        # print(result_list)
        mean_value = mean(result_list)
        # plain_val = "%f" % mean_value
        # print(plain_val)
        print(
            f"Durchschnitts-Zeitwert über {iterations_i} Testläufe mit {threads} Threads: {mean_value}\n"
        )

    # calculate table row ranges according to the thread numbers
    def calc_borders(entry, rows, threads):
        last_entry = entry
        for thread in range(threads):
            if last_entry == entry:
                next_border = last_entry + (rows // threads) - 1
            else:
                next_border = last_entry + (rows // threads)
            t = Thread(target=read_range, args=(last_entry, next_border))
            t.start()
            last_entry = next_border + 1

    def each_thread(rows, threads):
        # prevent reading more table lines than existing
        # with the floor division operator, rounding
        # float values to the next lower integer
        each_th = rows // threads
        print(f"With {threads} each thread handles {each_th}.")
        return each_th

    # print("Choose a desired thread count")
    # each_thread(ROW_COUNT, TH_LOW)
    # each_thread(ROW_COUNT, TH_MED)
    # each_thread(ROW_COUNT, TH_HIG)

    # important - deactivate test functions below line 129!
    # activate prints for count table and query content
    # in function def print_all_data in database.py
    #dbms.count_query()
    # activate prints for query content and more query content
    # in function def print_all_data in database.py
    #dbms.print_all_data(database.TABLE)

    # *Zeitmessung mit Threading und Aufteilen der Lesezugriffe

    results_threaded = []
    i = 800
    # change TH_<priority> to LOW or MED or HIG
    th_cat = TH_LOW

    threaded_testcase(i, results_threaded, th_cat)
    show_results(i, results_threaded, th_cat)


# run the program
if __name__ == "__main__":
    main()
