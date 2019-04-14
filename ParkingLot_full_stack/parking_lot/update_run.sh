#!/bin/bash 
cd ./db_frontend
# fix for docker changing the own to ./dist
sudo chown -R kevin:kevin ./dist ./node_modules ../static
yarn run build:prod
cd -
pipenv run python manage.py collectstatic --clear
pipenv run python manage.py migrate
# 因为 Django 在 debug 为 False 的时候不再提供静态文件的服务,
# 一般是要交给 nginx 来做, 不过这里为了方便, 还是用 Django的
# 这时候需要指定 --insecure
pipenv run ./manage.py runserver 0.0.0.0:8080 --insecure
