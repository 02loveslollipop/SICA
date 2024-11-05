#!/bin/bash
# Run the tests
echo "Starting conda environment"
conda init
conda activate SICA
echo "Starting the API"
python main.py &
echo "waiting 5 seconds for the API to start"
sleep 5
echo "Running the tests"
pytest apiTest.py -v -s
echo "Killing the API"
pkill -f main.py
echo "Deactivating the conda environment"
conda deactivate

