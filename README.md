# Multiprocessing task using Python
This project demonstrates a simple metrics aggregation system using multiprocessing
in Python. It consists of a master process and multiple worker processes that generate
and send metric data to the master. The master aggregates and logs the metrics every
10 seconds and 60 seconds.
## Clone the repository:
git clone https://github.com/dan9Protasenia/Multiprocessing_task cd Multiprocessing_task
## Usage
### 1. Run the master process:
`python main.py`
- The master process will start listening for worker messages.
### 2. Monitor the logs:
The master logs aggregated metrics every 10 seconds and 60 seconds.
### 3. Terminate the processes:
Press `Ctrl + C` in the terminal where the master is running to terminate both the master and worker processes.
## Configuration
You can customize the number of worker processes and the output file for metrics in the main.py file.<br>
![image](https://github.com/dan9Protasenia/Multiprocessing_task/assets/100715839/f1dfdb37-adca-473e-83be-ec7296a2ce8b)
