# HTW M1 Softwarearchitecture

## Getting started

Before running the demo, the following tools must be installed on the system:
- [Docker](https://www.docker.com/get-started)
- [NodeJS](https://nodejs.org/en/)
- [Python](https://www.python.org/downloads/)

Install the required python dependencies:
```bash
sudo python3 -m pip install -r requirements.txt
# Or use a virtual environment
```

Install the dependancies of the web interface:
```bash
npm i --prefix website
```

Finally, run the start script:
```bash
./start.sh
```
When the warm up is finished, the overview can be seen on http://localhost:5000

## Set up
### Create the Virtual Environment for python

```bash
# Create Venv 
python3 -m venv .venv
# Use the virtual environment
source .venv/bin/activate
# Install listed dependencies
sudo python3 -m pip install -r requirements.txt
# Export dependencies
python3 -m pip freeze > requirements.txt
# Exit Virtual env
deactivate
```

### Install web interface dependencies
Init: `npm i --prefix website`


### Launch the λ

Automatic launch: `./start.sh`

---
Manual Launch:
Build cassandra image: `docker build -t cassandra-batch src/batch`  
Run cassandra image: `docker run -d -p 9042:9042 --name cassandra_b cassandra-batch`

Launch sender: `python3 -m src.entry.sender`
Launch receiver: `python3 -m src.entry.receiver`
Run Batch processing and start producing the views into the serving: `python3 -m src.batch.BatchProcessing`

### Launch overview dashboard
Launch API: `cd src && sudo python3 -m flask run --host=127.0.0.1 --port=2020`
serve dashboard: `npm run dev --prefix website`


(Run PySpark : `python src/batch/pyspark-processing`)