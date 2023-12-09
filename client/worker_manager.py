import multiprocessing
from worker import worker


def run_workers(master_address, num_workers):
    try:
        workers = start_workers(master_address, num_workers)
        for worker_process in workers:
            worker_process.join()

    except KeyboardInterrupt:
        stop_workers(workers)


def start_workers(master_address, num_workers):
    worker_processes = []

    for i in range(num_workers):
        worker_port = master_address[1] + i
        worker_process = multiprocessing.Process(target=worker, args=(worker_port, master_address))
        worker_processes.append(worker_process)
        worker_process.start()

    return worker_processes


def stop_workers(worker_processes):
    for worker_process in worker_processes:
        worker_process.terminate()
        worker_process.join()
