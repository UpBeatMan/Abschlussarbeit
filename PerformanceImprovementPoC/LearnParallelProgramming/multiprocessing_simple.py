import multiprocessing


def worker(num):
    # * thread worker function
    print(f"worker: {num}")
    return


if __name__ == "__main__":
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

#! apparently the multiprocessing sequence is out of order - some times!
