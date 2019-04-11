#!/bin/bash 
python3 -m pipenv install && python3 -m pipenv run python ./manage.py migrate
