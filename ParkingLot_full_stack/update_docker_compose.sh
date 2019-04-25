#!/bin/bash
# rebuild docker containers
cd ./parking_lot && pipenv run python -c 'from pipenv_to_requirements import main; main()' -f && cd ../ && docker-compose -f ./docker-compose.yml up --build 
