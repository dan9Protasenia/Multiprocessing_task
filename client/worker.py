import socket
import json
import logging
import time


def worker(worker_port, master_address):
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s : %(message)s'
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", worker_port))
    logging.info(f"Worker started. Port {worker_port}")

    A1_value = 0
    A2_value = 0
    A3_value = 0

    try:
        while True:
            A1_value += 1
            A2_value += 2
            A3_value += 3
            message = {"A1": A1_value, "A2": A2_value, "A3": A3_value}

            sock.sendto(json.dumps(message).encode(), master_address)
            logging.info(f"Sent message to master: {message}")

            # time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Worker terminated")

    finally:
        sock.close()
