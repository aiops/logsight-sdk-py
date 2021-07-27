#!/bin/bash

PYTHONPATH="/home/jcardoso/Code/logsight-python-sdk/"
export PYTHONPATH

python -m unittest test_app_mng.TestAppManagement
python -m unittest test_hello_app.TestHelloApp
