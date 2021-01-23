from flask import Flask, jsonify
from .serving.CassandraWrapper import CassandraWrapper as ServingCassandraWrapper
from .batch.CassandraWrapper import CassandraWrapper as BatchCassandraWrapper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

servingCassandra = ServingCassandraWrapper()
batchCassandra = BatchCassandraWrapper()

def getSpamsFromView():
    return servingCassandra.execute("select * from spamsCounterLog;")
def getEmailsCountNumber():
    return batchCassandra.execute("select count(*) from emails;")._current_rows[0].count
def getSpamsAmountDetectedBySpeed():
    return servingCassandra.execute("select * from spamAmountDetectedBySpeed;")

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


@app.route('/speed/spams/count')
def spamsAmountDetectedBySpeed():
    counts = []
    spamsDetectedResponse = getSpamsAmountDetectedBySpeed()
    spamsDetectedResponseCount = len(spamsDetectedResponse._current_rows)

    for i in range(spamsDetectedResponseCount):
        spamResponse = spamsDetectedResponse._current_rows[i]
        count = spamResponse.spamcount
        counts.append(count)

    counts.sort()
    latestCountValue = counts[-1]
    return jsonify({"count": latestCountValue})

@app.route('/emails/count')
def emailsCount():
    return jsonify({"count": getEmailsCountNumber()})
