# HTW M1 Softwarearchitecture

## Set up
## Virtual Environment for python
```bash
# Create Venv 
python3 -m venv .venv
# Use the virtual environment
source .venv/bin/activate
# Install listed dependencies
sudo python3 -m pip install -r requirements.txt
# Export dependancies
python3 -m pip freeze > requirements.txt
# Exit Virtual env
deactivate
```

## Init dashboard website
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