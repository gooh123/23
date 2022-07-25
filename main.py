import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(it, cmd, value):
    res = map(lambda v: v.strip(), it)
    if cmd == 'filter':
        res = filter(lambda v: value in v.strip(), res)
    if cmd == 'sort':
        res = sorted(res, reverse=value)
    if cmd == 'unique':
        res = set(res)
    if cmd == 'limit':
        value = int(value)
        res = list(res[:value])
    if cmd == 'map':
        value = int(value)
        res = map(lambda v: v.split(' ')[value], res)
    return res


@app.route("/perform_query")
def perform_query():
    try:
        cmd_1 = request.args['cmd_1']
        cmd_2 = request.args['cmd_2']
        val_1 = request.args['val_1']
        val_2 = request.args['val_2']
        file_name = request.args['file_name']
    except:
        return BadRequest

    path_File = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_File):
        return BadRequest

    with open(path_File) as f:
        res = build_query(f, cmd_1, val_1)
        res = build_query(res, cmd_2, val_2)

    return app.response_class(res, content_type="text/plain")

