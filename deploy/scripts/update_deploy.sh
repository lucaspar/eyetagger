#!/usr/bin/env bash

# install new packages
yarn install
pipenv install

# create build files
yarn build
pipenv run ./manage.py collectstatic --no-input

# run new migrations
pipenv run ./manage.py makemigrations && \
pipenv run ./manage.py migrate

# setting gunicorn
cp deploy/gunicorn.service.root /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo service gunicorn restart
sudo service gunicorn enable

# setting nginx
cp deploy/default /etc/nginx/sites-available/default
sudo service nginx restart
