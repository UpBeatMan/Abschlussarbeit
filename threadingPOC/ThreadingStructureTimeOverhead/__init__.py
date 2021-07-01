from statistics import mean
from timeit import Timer
from threading import Thread

__version__ = "0.1.0"

# thread count
TH_LOW: int = 2
TH_MED: int = 4
TH_HIG: int = 8
TH_EXT: int = 16


def main():
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
    def start_threads(threads):
        for thread in range(threads):
            t = Thread(target=do_nothing, args=())
            t.start()

    def do_nothing():
        pass

    def threaded_testcase(iterations_i, result_list, th_cat):
        for loop in range(iterations_i):
            # with threading module
            t = Timer(lambda: start_threads(th_cat))
            time = t.timeit(number=1)
            print(
                f"ThreadOverhead: Zeitmessung mit {th_cat} Threads in ns - Durchlauf {loop + 1}: {time}"
            )
            result_list.append(time)
        return results_thread_startonly

    def show_results(iterations_i, result_list):
        # print("\n")
        print(result_list)
        mean_value = mean(result_list)
        # plain_val = "%f" % mean_value
        # print(plain_val)
        print(f"Durchschnittswert über {iterations_i} Testläufe: {mean_value}\n")

    i = 50
    results_thread_startonly = []

    # print("Zeitmessung der Threaderstellung ohne SQL-Logik.")
    threaded_testcase(i, results_thread_startonly, TH_LOW)
    show_results(i, results_thread_startonly)


# run the program
if __name__ == "__main__":
    main()
