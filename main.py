import json
import logging
import socket
import time
import signal
import sys
from multiprocessing import Process, Queue

from constant import LOCAL_HOST, MASTER_PORT
from tools import log_metrics, setup_logger


class Worker:
    def __init__(self, worker_port, master_address, message_queue):
        self.worker_port = worker_port
        self.master_address = master_address
        self.message_queue = message_queue

    def start(self):
        setup_logger()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((LOCAL_HOST, self.worker_port))
        logging.info(f"Worker started. Port {self.worker_port}")

        A1_value = 0
        A2_value = 0
        A3_value = 0

        try:
            while True:
                A1_value += 1
                A2_value += 2
                A3_value += 3
                message = {"A1": A1_value, "A2": A2_value, "A3": A3_value}

                sock.sendto(json.dumps(message).encode(), self.master_address)
                logging.info(f"Sent message to master: {message}")
                time.sleep(1)

        except KeyboardInterrupt:
            logging.info("Worker terminated")
        finally:
            sock.close()


class Master:
    def __init__(self, num_workers, output_file="metrics.json"):
        self.num_workers = num_workers

        self.metric_data_10s = {"A1_sum": 0, "A2_max": 0, "A3_min": float('inf')}
        self.metric_data_60s = {"A1_sum": 0, "A2_max": 0, "A3_min": float('inf')}

        self.sock = self.setup_socket()
        self.output_file = output_file
        self.message_queue = Queue()

        logging.info(f"Master started. Port {MASTER_PORT}")

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((LOCAL_HOST, MASTER_PORT))
        return self.sock

    def process_message(self, message):
        self.metric_data_10s["A1_sum"] += message["A1"]
        self.metric_data_10s["A2_max"] = max(self.metric_data_10s["A2_max"], message["A2"])
        self.metric_data_10s["A3_min"] = min(self.metric_data_10s["A3_min"], message["A3"])

        self.metric_data_60s["A1_sum"] += message["A1"]
        self.metric_data_60s["A2_max"] = max(self.metric_data_60s["A2_max"], message["A2"])
        self.metric_data_60s["A3_min"] = min(self.metric_data_60s["A3_min"], message["A3"])

    def log_metrics(self, count_type, metric_data, output_file):
        log_metrics(count_type, metric_data, output_file)

    def worker_process(self, worker):
        worker.start()

    def start(self):
        logging.getLogger().setLevel(logging.INFO)
        setup_logger()

        worker_port = 12345
        workers = [Worker(worker_port, (LOCAL_HOST, MASTER_PORT), self.message_queue) for _ in range(self.num_workers)]
        worker_processes = [Process(target=self.worker_process, args=(worker,)) for worker in workers]

        def handle_termination(signal, frame):
            logging.info("Terminating Master and Workers...")
            for process in worker_processes:
                process.terminate()
            self.sock.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_termination)

        try:
            for process in worker_processes:
                process.start()

            while True:
                message, _ = self.sock.recvfrom(1024)
                message = json.loads(message.decode())
                self.process_message(message)

                current_time = int(time.time())
                if current_time % 10 == 0:
                    self.log_metrics("10s", self.metric_data_10s, self.output_file)

                if current_time % 60 == 0:
                    self.log_metrics("60s", self.metric_data_60s, self.output_file)

        except KeyboardInterrupt:
            logging.info("Master terminated")

        finally:
            for process in worker_processes:
                process.terminate()

            self.sock.close()


if __name__ == "__main__":
    num_workers = 3
    master = Master(num_workers)
    master.start()
