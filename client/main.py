from worker_manager import run_workers
from Multiprocessing_task.constant import LOCAL_HOST

if __name__ == "__main__":
    master_address = (LOCAL_HOST, 9091)
    num_workers = 5
    run_workers(master_address, num_workers)
