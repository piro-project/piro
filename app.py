import rackset
import logging
import logzero
from logzero import logger
from flask import Flask, render_template, jsonify
app = Flask(__name__)

logzero.loglevel(logging.INFO)
racks = rackset.rackset()
racks.load_racks_from_file('config.yaml')
@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/random")
def random():
    return render_template("random.html")

@app.route("/health")
def healthCheck():
    return '{"status": "piro API is up"}'

@app.route("/rackset/load/<filename>")
def loadRackset(filename):
    racks.load_racks_from_file(filename)
    return '{"status": "rackset loaded."}'

@app.route("/rackset/status")
def racksetStatus():
    return jsonify(racks.status())

@app.route("/rackset/fire")
def fireList():
    return jsonify(racks.fire_list())

@app.route("/rackset/fire/<rack>/<channel>")
def fireChannel(rack, channel):
    racks.fire_channel(int(rack), int(channel))
    return '{"status": "channel fired."}'

@app.route("/rackset/fire/random", methods = ['PUT', 'GET', 'POST'])
def fireRandom():
    racks.fire_random()
    return '{"status": "channel fired."}'