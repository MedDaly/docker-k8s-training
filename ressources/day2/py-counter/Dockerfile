FROM python:3.9-slim

RUN pip install argparse
RUN pip install time

COPY main.py /app/main.py

WORKDIR /app

ARG N=60

ENV LOG_FILE="default_log.txt"

ENTRYPOINT ["python", "main.py", "--n", "$N"]
