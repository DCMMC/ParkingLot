#!/usr/bin/env bash
# init file
set -e

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    echo 'migrate datebase'
    pipenv run ./parking_lot/manage.py makemigrations --noinput && pipenv run ./parking_lot/manage.py migrate --noinput
fi

if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    echo 'collect static'
    cd ./parking_lot/db_frontend && yarn install && yarn run build && cd -
    pipenv run ./parking_lot/manage.py collectstatic --noinput
fi

exec "$@"
