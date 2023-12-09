from worker import worker

import multiprocessing

if __name__ == "__main__":
    master_address = ("localhost", 9091)

    worker_processes = []

    for i in range(50):
        worker_port = 9090 + i
        worker_process = multiprocessing.Process(target=worker, args=(worker_port, master_address))
        worker_processes.append(worker_process)
        worker_process.start()

    try:
        for worker_process in worker_processes:
            worker_process.join()

    except KeyboardInterrupt:
        for worker_process in worker_processes:
            worker_process.terminate()
            worker_process.join()
