# htw-m1-softwarearchitecture

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
# Exit venvdocker
deactivate
```

### Batch Layer
Build cassandra image: `docker build -t cassandra-batch src/batch`  
Run cassandra image: `docker run -d -p 9042:9042 --name cassandra_b cassandra-batch`  