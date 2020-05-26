#!/usr/bin/bash
# Deploy script for annotation tool

set -e

APP_HOME=/app
cd $APP_HOME

# install gsutil
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt install -y apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt update && sudo apt install -y google-cloud-sdk

# install yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update && sudo apt install -y yarn

# install pipenv
sudo apt purge -y python-pip            # remove pip for python2
sudo apt install -y python3 python3-pip
pip install --upgrade pip
pip install pipenv
sudo ln -s $(which pip3) /usr/bin/pip

# install project dependencies
yarn install
pipenv install

# build front-end files
yarn build

# install postgres
echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" | sudo tee -a /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt install -y postgresql-12
cp deploy/db_creation.sql /tmp/ && chown postgres:postgres /tmp/db_creation.sql
chmod a+r /tmp/db_creation.sql
echo "Please, write '\i db_creation.sql' in this shell, then '\q' to quit:"
# psql -f db_creation.sql
cd /tmp
sudo -u postgres psql
cd $APP_HOME

# create dotenv
cp backend/settings/.env.example backend/settings/.env
nano backend/settings/.env

# build back-end files
pipenv shell
./manage.py collectstatic

# create google bucket credentials
mkdir -p $APP_ROOT/.gcp/
touch $APP_ROOT/.gcp/iris-admin.json
chmod 600 $APP_ROOT/.gcp/iris-admin.json
echo -e "Paste the contents of the GCP JSON here.\nSee https://cloud.google.com/docs/authentication/getting-started"
nano $APP_ROOT/.gcp/iris-admin.json
chmod 400 $APP_ROOT/.gcp/iris-admin.json
export GOOGLE_APPLICATION_CREDENTIALS="$APP_ROOT/.gcp/iris-admin.json"
echo 'export GOOGLE_APPLICATION_CREDENTIALS="$APP_ROOT/.gcp/iris-admin.json"' >> ~/.bashrc

# prepare data
dvc pull
ln -s $(pwd)/backend/dataset $(pwd)/dist/static/data

# migrate database
./manage.py migrate
echo "Create the superuser now, but don't forget the password!"
./manage.py createsuperuser

# copy gunicorn configuration
cp deploy/gunicorn.service.root /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo service gunicorn restart

# install nginx
nginx=stable # use nginx=development for latest development version
sudo add-apt-repository -y ppa:nginx/$nginx
sudo apt update
sudo apt install -y nginx

# replace nginx configuration
sudo service nginx start
cp deploy/default /etc/nginx/sites-available/default
sudo service nginx restart

# create static files symbolic link
mkdir -p /var/www/iris
ln -s /app/dist /var/www/iris/common

# fix permissions
chmod +x /var/www/iris/
chmod +x /var/www/
sudo chgrp -R www-data /var/www/iris/
sudo chgrp -R www-data /var/www/iris/
sudo chown -R www-data: /var/www/iris/

# example of working permissions:
#
#   root@iris-webapp:/app# namei -l /var/www/iris/common/static/favicon.ico
#       f: /var/www/iris/common/static/favicon.ico
#       drwxr-xr-x root     root     /
#       drwxr-xr-x root     root     var
#       drwxrwx--x root     www-data www
#       drwxrwsr-x www-data www-data iris
#       lrwxrwxrwx www-data www-data common -> /app/dist
#       drwxr-xr-x root     root       /
#       drwxr-xr-x www-data www-data   app
#       drwxr-xr-x www-data www-data   dist
#       drwxr-xr-x www-data www-data static
#       -rw-r--r-- www-data www-data favicon.ico


# debugging nginx:
# tail -n 50 /var/log/nginx/iris.error.log

# debugging gunicorn:
# sudo journalctl -u gunicorn | tail -n 50
