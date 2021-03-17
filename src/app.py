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
def getSpamsAmountDetectedByBatchResponse():
    return servingCassandra.execute("select * from spamEmailAmountDetectedByBatch;")
def getSpamsAmountDetectedBySpeedResponse():
    return servingCassandra.execute("select * from spamEmailAmountDetectedBySpeed;")
def getSpamsAmountDetectedBySpeed():
    counts = []
    spamsDetectedResponse = getSpamsAmountDetectedBySpeedResponse()
    spamsDetectedResponseCount = len(spamsDetectedResponse._current_rows)

    noSpamsDetected = spamsDetectedResponseCount <= 0
    if noSpamsDetected:
        return 0

    for i in range(spamsDetectedResponseCount):
        spamResponse = spamsDetectedResponse._current_rows[i]
        count = spamResponse.spamcount
        counts.append(count)

    counts.sort()
    return counts[-1]

def getSpamsAmountDetectedByBatch():
    counts = []
    spamsDetectedResponse = getSpamsAmountDetectedByBatchResponse()
    spamsDetectedResponseCount = len(spamsDetectedResponse._current_rows)

    for i in range(spamsDetectedResponseCount):
        spamResponse = spamsDetectedResponse._current_rows[i]
        count = spamResponse.spamcount
        counts.append(count)

    counts.sort()
    return counts[-1]
    

# Spams sender count history
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
    return jsonify({"count": getSpamsAmountDetectedBySpeed()})

@app.route('/difference/batch-speed/spams/count')
def differenceSpamsAmountDetected():
    return jsonify({"speed": getSpamsAmountDetectedBySpeed(), "batch": getSpamsAmountDetectedByBatch()})

@app.route('/emails/count')
def emailsCount():
    return jsonify({"count": getEmailsCountNumber()})
