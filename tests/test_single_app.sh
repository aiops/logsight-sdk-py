#!/bin/bash

PYTHONPATH="/home/jcardoso/Code/logsight-python-sdk/"
export PYTHONPATH

for i in $(seq 20)
do
   now=$(date)
   echo "Test number: $i ($now)"
   python -m unittest test_single_app.TestSingleApp
   SECONDS=60
   echo "Sleeping $SECONDS"
   sleep $SECONDS
done

