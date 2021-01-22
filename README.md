# HTW M1 Softwarearchitecture

## Set up
## Virtual Environment for python
```bash
# Create Venv 
python -m venv .venv
# Use the virtual environment
source .venv/bin/activate
# Install listed dependencies
python -m pip install -r requiremetns.txt
# Export dependancies
python -m pip freeze > requirements.txt
# Exit Virtual env
deactivate
```

### Launch the λ

Build cassandra image: `docker build -t cassandra-batch src/batch`  
Run cassandra image: `docker run -d -p 9042:9042 --name cassandra_b cassandra-batch`

Launch sender: `python -m src.entry.sender`
Launch receiver: `python -m src.entry.receiver`
Run Batch processing and start producing the views into the serving: `python -m src.batch.BatchProcessing`


(Run PySpark : `python src/batch/pyspark-processing`)