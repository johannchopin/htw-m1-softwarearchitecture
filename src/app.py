from flask import Flask
from .serving.CassandraWrapper import CassandraWrapper
import json

app = Flask(__name__)

cassandra = CassandraWrapper()

@app.route('/spams')
def hello_world():
    spams = {}
    spamsResponse = cassandra.execute("select * from spamsCounterLog;")
    spamsResponseCount = len(spamsResponse._current_rows)

    for i in range(spamsResponseCount):
        spamResponse = spamsResponse._current_rows[i]
        timestamp = spamResponse.timestamp
        count = spamResponse.spamcount
        spams[timestamp] = count

    return json.dumps(spams)
