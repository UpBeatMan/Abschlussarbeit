# !/usr/bin/env python
#!-*- coding: utf-8 -*-
# * for ChromeModel

from threading import Thread
from statistics import mean
from timeit import Timer
import os
import shutil
import database

__version__ = "0.2.2"

# * choose thread count
TH_LOW: int = 2
TH_MED: int = 4
TH_HIG: int = 8
TH_EXT: int = 16

# ! edit windows user name !
USERNAME = "Yochanan"
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
# count_query() result - static test variable
ROW_COUNT = 107
# first id in table - static test variable
START_ID: int = 1


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

    def threaded_testcase(iterations_i, result_list, th_cat):
        for loop in range(iterations_i):
            # with threading module
            t = Timer(lambda: calc_borders(START_ID, ROW_COUNT, th_cat))
            time = t.timeit(number=1)
            # print(
            #     f"Zeitmessung mit {th_cat} Threads in ns - Durchlauf {loop + 1}: {time}"
            # )
            result_list.append(time)
        return result_list

    def show_results(iterations_i, result_list):
        # print("\n")
        # print(result_list)
        mean_value = mean(result_list)
        # plain_val = "%f" % mean_value
        # print(plain_val)
        print(f"Durchschnittswert über {iterations_i} Testläufe: {mean_value}\n")

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

    def each_thread(rows, th_cat):
        # Es wird nach unten gerundet. Für den Test vorerst irrelevant!
        each_th = rows // th_cat
        print(f"With {th_cat} each thread handles {each_th}.")
        return each_th

    # print("Choose a desired thread count")
    # each_thread(ROW_COUNT, TH_LOW)
    # each_thread(ROW_COUNT, TH_MED)
    # each_thread(ROW_COUNT, TH_HIG)
    # each_thread(ROW_COUNT, TH_EXT)

    # show table content - activate print(row) in database.py
    # important - deactivate test functions below!
    # dbms.print_all_data(database.TABLE)

    # *Zeitmessung mit Threading und Aufteilen der Lesezugriffe

    results_threaded = []
    i = 800

    # ! change TH_<priority> to LOW, MED, HIG, EXT !
    threaded_testcase(i, results_threaded, TH_LOW)
    show_results(i, results_threaded)


# run the program
if __name__ == "__main__":
    main()
