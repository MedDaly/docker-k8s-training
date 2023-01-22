from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
from pathlib import Path
import socket
import random
import json
import logging

NOTES_PATH = Path("notes.txt")

hostname = socket.gethostname()

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def read_notes(path_):
    with open(path_, 'r') as f:
        lines = f.readlines()
    notes = [line.strip('\n') for line in lines]
    return notes

def add_note(note, path_):
    note = note.strip('\n')
    if path_.exists():
        with open(path_, 'a') as f:
            f.write(note+'\n')
    else:
        with open(path_, 'w') as f:
            f.write(note+'\n')

@app.route("/", methods=['POST','GET'])
def main():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    message = ''

    if request.method == 'POST':
        note = request.form['note']
        app.logger.info('Received new note : %s', note)
        add_note(note, NOTES_PATH)
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
    notes_list = []
    if NOTES_PATH.exists():
        notes_list = read_notes(NOTES_PATH)
    resp = make_response(render_template(
        'list.html',
        hostname=hostname,
        notes_list=notes_list
    ))
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
