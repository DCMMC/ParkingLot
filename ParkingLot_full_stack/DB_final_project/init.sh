#!/bin/bash 
python3 -m pipenv install --skip-lock && python3 -m pipenv run python ./parking_lot/manage.py migrate
