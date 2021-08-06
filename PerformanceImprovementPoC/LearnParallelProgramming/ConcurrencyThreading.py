# import threading
import concurrent.futures
import time


start = time.perf_counter()


def do_something(seconds):
    print(f"Sleeping {seconds} seconds(s)...")
    time.sleep(seconds)
    return f"Done Sleeping...{seconds}"


with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]

    # result = executor.map(do_something, secs)
    # for result in result:
    #     print(result)

    results = [executor.submit(do_something, sec) for sec in secs]
    for f in concurrent.futures.as_completed(results):
        print(f.result())


