FROM ubuntu:bionic

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ========
#  SYSTEM
# ========

# show distro and update from repos
RUN cat /etc/os-release
RUN apt-get update
RUN apt-get install -y curl

# locale setup
RUN apt-get install -y locales && locale-gen "en_US.UTF-8"
ENV LANG='en_US.UTF-8' LANGUAGE='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# install python and pipenv
RUN apt-get purge -y python-pip
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y python3.8 python3.8-dev python3.8-distutils python3.8-venv
RUN ln -s $(which pip3) /usr/bin/pip
RUN pip install --upgrade pip
RUN pip install pipenv

# install gsutil
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt-get install -y apt-transport-https ca-certificates gnupg
RUN export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update && apt-get install -y google-cloud-sdk

# install node
ENV NODE_VERSION=12.16.3
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version

# install yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn

# =========
#  PROJECT
# =========

# install project dependencies
COPY Pipfile Pipfile.lock package.json yarn.lock ./
RUN pipenv install
RUN yarn && yarn install

# copy other project files
COPY . .

# build static files
RUN pipenv run ./manage.py collectstatic --no-input
RUN yarn upgrade
RUN yarn build --no-clean

# run new migrations and serve app
CMD pipenv run ./manage.py makemigrations && \
    pipenv run ./manage.py migrate && \
    pipenv run ./manage.py runserver 0.0.0.0:8000
