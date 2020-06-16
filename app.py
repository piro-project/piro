import rackset
import logging
import logzero
from logzero import logger
from flask import Flask, render_template, jsonify,  send_from_directory
app = Flask(__name__)

logzero.loglevel(logging.INFO)
racks = rackset.rackset()
# racks.load_racks_from_file('config.yaml')
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def random():
    return render_template("random.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)

@app.route("/health")
def healthCheck():
    return '{"status": "piro API is up"}'

@app.route("/rackset/load/<filename>", methods = ['POST'])
def loadRackset(filename):
    racks.load_racks_from_file(filename)
    return '{"status": "rackset loaded."}'

@app.route("/rackset/status")
def racksetStatus():
    return jsonify(racks.status())

@app.route("/rackset/fire")
def fireList():
    return jsonify(racks.fire_list())

@app.route("/rackset/fire/<rack>/<channel>", methods = ['POST'])
def fireChannel(rack, channel):
    fired_channel = racks.fire_channel(int(rack), int(channel))
    response = jsonify(fired_rack = int(rack),
                        fired_channel = int(fired_channel),
                        status = "Firing rack: {rack} channel: {channel}".format(rack = rack, channel = fired_channel),
                        nice_status = "Firing {desc}".format(desc = racks.rack_array[int(rack)].descriptions[int(fired_channel)]))
    return response

@app.route("/rackset/fire/random", methods = ['POST'])
def fireRandom():
    fired_rack, fired_channel = racks.fire_random()
    response = jsonify(fired_rack = int(fired_rack),
                        fired_channel = int(fired_channel),
                        status = "Firing rack: {rack} channel: {channel}".format(rack = fired_rack, channel = fired_channel),
                        nice_status = "Firing {desc}".format(desc = racks.rack_array[int(fired_rack)].descriptions[int(fired_channel)]))
    return response

@app.route("/rackset/reset", methods = ['POST'])
def reset():
    racks.reset()
    return jsonify(nice_status = "all fired_states reset")