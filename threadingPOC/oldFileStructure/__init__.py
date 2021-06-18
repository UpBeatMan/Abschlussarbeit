from statistics import mean
from timeit import Timer
from database import database
from threading import Thread

__version__ = '0.2.0'

# thread count
TH_LOW: int = 2
TH_MED: int = 4
TH_HIG: int = 8
TH_EXT: int = 16

# table names
HISTORY: str = "moz_formhistory"
# count_query() result - static test variable
ROW_COUNT: int = 235
# first id in table - static test variable
START_ID: int = 1190


def main():
    dbms = database.MyDatabase(database.SQLITE, dbname='mydb.sqlite')
    dbms.count_query()

    def each_thread(rows, th_cat):
        # Es wird nach unten gerundet. Für den Test vorerst irrelecant!
        each_th = rows // th_cat
        print(f"With {th_cat} each thread handles {each_th}.")
        return each_th

    def end_range(rows, entry):
        endpoint = entry + (rows - 1)
        print(f"End row of all threads: {endpoint} \n")
        return endpoint

    # Functions
    # calculate table row ranges according to the thread numbers
    def calc_borders(entry, rows, threads):
        last_entry = entry
        for thread in range(threads):
            if last_entry == entry:
                next_border = last_entry + (rows // threads) - 1
            else:
                next_border = last_entry + (rows // threads)
            # print(f"Thread number: {thread}")
            # print(f"Begin range: {last_entry}")
            # print(f"End range: {next_border}\n")
            t = Thread(target=read_range, args=(last_entry, next_border))
            t.start()
            last_entry = next_border + 1

    def read_range(start, end):
        build = "SELECT * FROM {TBL_HST} WHERE id BETWEEN " + str(start) + " AND " + str(end) + ";"
        # print(build)
        query = build.format(TBL_HST=HISTORY)
        dbms.print_all_data(query=query)

    def threaded_testcase(iterations_i, result_list, th_cat):
        for loop in range(iterations_i):
            # with threading module
            t = Timer(lambda: calc_borders(START_ID, ROW_COUNT, th_cat))
            time = t.timeit(number=1)
            print(f"Zeitmessung mit {th_cat} Threads in ns - Durchlauf {loop + 1}: {time}")
            result_list.append(time)
        return result_list

    def nonthreaded_testcase(iterations_i, result_list):
        for loop in range(iterations_i):
            # with threading module
            t = Timer(lambda: read_range(START_ID, max_range))
            time = t.timeit(number=1)
            print(f"Zeitmessung ohne Threading in ns - Durchlauf {loop + 1}: {time}")
            result_list.append(time)
        return result_list

    def show_results(iterations_i, result_list):
        # print("\n")
        print(result_list)
        mean_value = mean(result_list)
        # plain_val = "%f" % mean_value
        # print(plain_val)
        print(f"Durchschnittswert über {iterations_i} Testläufe: {mean_value}\n")

    # timeit() normal vs threaded read access

    # first try - not working yet! -> static variable row_count for test
    # dbms.count_all_rows()

    # dbms.print_all_data(database.HISTORY)
    # calc_borders(start_id, row_count, thread_count)
    # read_range(start_id, max_range)

    # print("Choose a desired thread count")
    # each_thread(ROW_COUNT, TH_LOW)
    # each_thread(ROW_COUNT, TH_MED)
    # each_thread(ROW_COUNT, TH_HIG)
    # each_thread(ROW_COUNT, TH_EXT)

    max_range = end_range(ROW_COUNT, START_ID)

    i = 50
    results_threaded = []
    results_nonthreaded = []

    # print("Mit Threading und Aufteilen der Lesezugriffe.")
    threaded_testcase(i,  results_threaded, TH_LOW)
    show_results(i, results_threaded)

    # print("Ohne Threading und Aufteilen der Lesezugriffe.")
    nonthreaded_testcase(i, results_nonthreaded)
    show_results(i, results_nonthreaded)


# run the program
if __name__ == "__main__": main()
