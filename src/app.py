from flask import Flask, jsonify
from .serving.CassandraWrapper import CassandraWrapper
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

cassandra = CassandraWrapper()

def getSpamsFromView():
    return cassandra.execute("select * from spamsCounterLog;")

@app.route('/spams/count')
def spams():
    spams = []
    spamsResponse = getSpamsFromView()
    spamsResponseCount = len(spamsResponse._current_rows)

    for i in range(spamsResponseCount):
        spam = {}
        spamResponse = spamsResponse._current_rows[i]
        timestamp = spamResponse.timestamp
        count = spamResponse.spamcount
        spam["timestamp"] = timestamp
        spam["count"] = count
        spams.append(spam)

    return jsonify(spams)

@app.route('/spams/count')
def spamsCounter():
    spamsResponse = getSpamsFromView()
    spamsResponseCount = len(spamsResponse._current_rows)

    return jsonify({"count": spamsResponseCount})