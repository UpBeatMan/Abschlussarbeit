from statistics import mean
from timeit import Timer
from database import database

__version__ = "0.2.0"

# table names
HISTORY: str = "moz_formhistory"
# count_query() result - static test variable
ROW_COUNT: int = 235
# first id in table - static test variable
START_ID: int = 1190


def main():
    dbms = database.MyDatabase(database.SQLITE, dbname="mydb.sqlite")
    dbms.count_query()

    def end_range(rows, entry):
        endpoint = entry + (rows - 1)
        print(f"End row of all threads: {endpoint} \n")
        return endpoint

    # Functions
    def read_range(start, end):
        build = (
            "SELECT * FROM {TBL_HST} WHERE id BETWEEN "
            + str(start)
            + " AND "
            + str(end)
            + ";"
        )
        # print(build)
        query = build.format(TBL_HST=HISTORY)
        dbms.print_all_data(query=query)

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

    # dbms.print_all_data(database.HISTORY)

    i = 50
    max_range = end_range(ROW_COUNT, START_ID)

    results_nonthreaded = []

    # print("Zeitmessung ohne Threading und Aufteilen der Lesezugriffe.")
    nonthreaded_testcase(i, results_nonthreaded)
    show_results(i, results_nonthreaded)


# run the program
if __name__ == "__main__":
    main()
