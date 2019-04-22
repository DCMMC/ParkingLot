#!/usr/bin/env bash
# init file
set -e

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    echo 'migrate datebase'
    python3 ./parking_lot/manage.py makemigrations --noinput && python3 ./parking_lot/manage.py migrate --noinput && python3 ./parking_lot/manage.py create_db
fi

if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    echo 'collect static'
    cd ./parking_lot/db_frontend && yarn install && yarn build:prod && cd -
    python3 ./parking_lot/manage.py collectstatic --noinput
fi

exec "$@"
