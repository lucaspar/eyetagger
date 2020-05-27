#!/usr/bin/env bash

# install new packages
yarn install
pipenv install

# create build files
yarn build
pipenv run ./manage.py collectstatic --no-input

# pull data and create symlink
pipenv run dvc pull
ln -s $(pwd)/backend/dataset $(pwd)/dist/static/data

# run new migrations
pipenv run ./manage.py makemigrations && \
pipenv run ./manage.py migrate

# setting gunicorn
cp deploy/gunicorn.service.root /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo service gunicorn restart

# setting nginx
cp deploy/default /etc/nginx/sites-available/default
sudo service nginx restart

