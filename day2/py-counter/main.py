import argparse
import time
import os

# parse the command-line argument for n
parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, default=60, help="number of seconds it takes to finish the counter")
args = parser.parse_args()
n = args.n

for i in range(1, n+1):
    print(i)
    time.sleep(1)

log_file = os.getenv("LOG_FILE", "log.txt")

with open(log_file, "w") as f:
    f.write(f"{time.time()} - N = {n}\n")