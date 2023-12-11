import json
import time
import logging


def write_metrics_to_file(self, metric_data):
    with open(self.output_file, mode='a') as file:
        file.write(json.dumps(metric_data) + '\n')


def log_metrics(self, count_type):
    current_time = int(time.time())
    metric_data = {
        "timestamp": current_time,
        "count_type": count_type,
        "A1_sum": self.metric_data_10s["A1_sum"],
        "A2_max": self.metric_data_10s["A2_max"],
        "A3_min": self.metric_data_10s["A3_min"]
    }
    logging.info(f"Metrics for {count_type}: {metric_data}")
    write_metrics_to_file(metric_data)
