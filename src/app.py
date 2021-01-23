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

@app.route('/emails/count')
def emailsCount():
    return jsonify({"count": getEmailsCountNumber()})
