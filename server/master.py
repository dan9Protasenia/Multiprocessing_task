import socket
import json
import logging
import time

METRICS_FILE = "metrics.json"


def write_to_file(metric_data, count_type, current_time):
    with open(METRICS_FILE, "a") as file:
        file.write(json.dumps({
            "timestamp": current_time,
            "count_type": count_type,
            "A1_sum": metric_data["A1_sum"],
            "A2_max": metric_data["A2_max"],
            "A3_min": metric_data["A3_min"]
        }) + '\n')


def master(master_port):
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s : %(message)s'
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", master_port))
    logging.info(f"Master started. Port {master_port}")

    metric_data_10s = {"A1_sum": 0, "A2_max": float('-inf'), "A3_min": float('inf')}
    metric_data_60s = {"A1_sum": 0, "A2_max": float('-inf'), "A3_min": float('inf')}
    start_time_10s = time.time()
    start_time_60s = time.time()

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())
            logging.info(f"Received message from {addr}: {message}")

            metric_data_10s["A1_sum"] += message["A1"]
            metric_data_10s["A2_max"] = max(metric_data_10s["A2_max"], message["A2"])
            metric_data_10s["A3_min"] = min(metric_data_10s["A3_min"], message["A3"])

            metric_data_60s["A1_sum"] += message["A1"]
            metric_data_60s["A2_max"] = max(metric_data_60s["A2_max"], message["A2"])
            metric_data_60s["A3_min"] = min(metric_data_60s["A3_min"], message["A3"])

            current_time = int(time.time())
            if current_time - start_time_10s >= 10:
                write_to_file(metric_data_10s, "10s", current_time)
                start_time_10s = current_time
                logging.info(f"spend 10 sec {current_time}")

            if current_time - start_time_60s >= 60:
                write_to_file(metric_data_60s, "60s", current_time)
                start_time_60s = current_time
                logging.info(f"spend 60 sec {current_time}")

    except KeyboardInterrupt:
        logging.info("Master terminated")
    finally:
        sock.close()
