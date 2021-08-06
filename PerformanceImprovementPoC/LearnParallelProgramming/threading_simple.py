import threading


def worker(num):
    # * thread worker function
    print(f"worker: {num}")
    return


if __name__ == "__main__":
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

#! apparently the multithreading sequence stays in order!
