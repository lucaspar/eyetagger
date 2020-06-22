#!/usr/bin/bash
# Deploy script for annotation tool

set -e

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
sudo apt purge -y python-pip
sudo apt install -y python3 python3-pip
sudo apt install -y python3.8 python3.8-dev python3.8-distutils python3.8-venv
pip install --upgrade pip
pip install pipenv
sudo ln -s $(which pip3) /usr/bin/pip

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
cd ~/app

# install project dependencies
yarn install
pipenv install

# create dotenv
cp backend/settings/.env.example backend/settings/.env
nano backend/settings/.env

# build static files
yarn build
pipenv run ./manage.py collectstatic

# create google bucket credentials
mkdir -p $HOME/.gcp/
touch $HOME/.gcp/iris-admin.json
chmod 600 $HOME/.gcp/iris-admin.json
echo -e "Paste the contents of the GCP JSON here.\nSee https://cloud.google.com/docs/authentication/getting-started"
nano $HOME/.gcp/iris-admin.json
chmod 400 $HOME/.gcp/iris-admin.json
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/iris-admin.json"
echo 'export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/iris-admin.json"' >> ~/.bashrc

# pull data and create symlink
pipenv run dvc pull
ln -s $(pwd)/backend/dataset $(pwd)/dist/static/data

# update deployed application
./update_deploy.sh
