import json
import time
import logging


def setup_logger():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )


def log_metrics(count_type, metric_data, output_file):
    current_time = int(time.time())
    metric_data["timestamp"] = current_time
    metric_data["count_type"] = count_type

    logging.info(f"Metrics for {count_type}: {metric_data}")

    with open(output_file, mode='a') as file:
        file.write(json.dumps({
            "timestamp": metric_data["timestamp"],
            "count_type": metric_data["count_type"],
            "A1_sum": metric_data["A1_sum"],
            "A2_max": metric_data["A2_max"],
            "A3_min": metric_data["A3_min"]
        }) + '\n')
