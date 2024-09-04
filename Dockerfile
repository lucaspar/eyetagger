FROM ubuntu:24.04

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ========
#  SYSTEM
# ========

# show distro and update from repos
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl

# locale setup
RUN apt-get install -y locales && locale-gen "en_US.UTF-8"
ENV LANG='en_US.UTF-8' LANGUAGE='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# install gsutil for integration with google cloud storage
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt-get install -y apt-transport-https ca-certificates gnupg
RUN export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update && apt-get install -y google-cloud-sdk

# install uv and python
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# install node
ENV NODE_VERSION=20.11.1
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.40.1/install.sh | bash
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

# copy other project files
COPY . .

# install project dependencies and run project from the script, so the
# env vars are properly set. Also run new migrations and serve app:
CMD scripts/install-and-run.sh
