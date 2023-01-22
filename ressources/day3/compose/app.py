from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
from pathlib import Path
import socket
import random
import json
import logging
import mysql.connector

LOG_FILE = Path("logs", "flask.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
LOG_FILE.touch(exist_ok=True)

hostname = socket.gethostname()

app = Flask(__name__)

# Set up a file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)

app.logger.setLevel(logging.INFO)

DB_HOST = os.getenv("DB_HOST", "my-db")

# DB connection parameters
CONN_PARAMS = {
    #"host": "localhost",
    #"host": "my-db",
    "host": DB_HOST,
    "port": 3306,
    "user": "root",
    "password": "admin",
    "database": "notesdb"
}

def read_notes():
    with mysql.connector.connect(**CONN_PARAMS) as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM NOTES")
        all_notes = cursor.fetchall()
    notes = [row['note'] for row in all_notes]
    app.logger.info(f"The total number of notes is {len(notes)}")
    return notes

def add_note(note):
    note = note.strip('\n')
    with mysql.connector.connect(**CONN_PARAMS) as conn:
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO NOTES (note) VALUES ("{note}")')
        conn.commit()
    app.logger.info('Received new note : %s', note)

@app.route("/", methods=['POST','GET'])
def main():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    message = ''

    if request.method == 'POST':
        note = request.form['note']
        add_note(note)
        message = "Note Saved !!"

    resp = make_response(render_template(
        'index.html',
        hostname=hostname,
        message=message
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


@app.route("/list", methods=['GET'])
def list():
    notes_list = read_notes()
    resp = make_response(render_template(
        'list.html',
        hostname=hostname,
        notes_list=notes_list
    ))
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
