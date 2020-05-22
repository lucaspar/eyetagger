# Iris Annotator

![Annotator Logo](/src/assets/logo-iris.png "Iris Annotator")

Annotation tool for iris images.

Used [this Vue + Django template](https://github.com/gtalarico/django-vue-template) as basis. Vue.js as a Single Page Application (SPA); and Django + PostgreSQL for the back-end, which communicates through a REST API with the front.

## Includes

+ Django web server
+ Django admin panel at `/api/admin/`
+ Django REST API
+ Django Whitenoise to serve static files, and CDN Ready
+ Vue CLI 3 to create the front-end
+ Vue Router for Single Page Application functionality
+ Vuex for state management and persistance to never lose annotations
+ Gunicorn - WSGI / translates HTTP requests into Python commands
+ Configuration for Heroku Deployment

## 1. Execution

### 1.1. Dependencies

Before getting started you should have the following installed and running:

+ Yarn - [instructions](https://yarnpkg.com/en/docs/install)
+ Vue CLI 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
+ Python 3 - [instructions](https://wiki.python.org/moin/BeginnersGuide)
+ Pipenv - [instructions](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
+ PostgreSQL - [instructions](https://www.postgresql.org/download/)

### 1.2. Setup Template

#### Install Packages

```sh
yarn install
pipenv install --dev && pipenv shell
```

#### Database

```sh
# create a symbolic link for your image dataset
ln -s /your/dataset/location    backend/dataset

# make sue PostgreSQL is running to store the annotations
service postgresql status

# database setup
sudo -u postgres psql
# an iteractive shell will open, then adapt and run the following commands:

# create database and user:
#=#     CREATE DATABASE annotation_tool;
#=#     CREATE USER annotator_admin WITH PASSWORD 'my_ultra_secure_db_password';

# adjust settings:
#=#     ALTER ROLE annotator_admin SET client_encoding TO 'utf8';
#=#     ALTER ROLE annotator_admin SET default_transaction_isolation TO 'read committed';
#=#     ALTER ROLE annotator_admin SET timezone TO 'UTC';
#           or America/Indiana/Indianapolis

# configure access control and quit
#=#     GRANT ALL PRIVILEGES ON DATABASE annotation_tool TO annotator_admin;
#=#     \q

# run database migrations
python manage.py migrate
```

### 1.3. Running Development Servers

#### Back-end

```sh
python manage.py runserver
# served from localhost:8000
```

#### Front-end

```sh
yarn serve
# open http://localhost:8080
```

Proxy config in [`vue.config.js`](/vue.config.js) is used to route the requests
back to django's API on port 8000.

## 2. Deploy

1. Independent of the deploy method, you need to set the correct environment for the back and front-end by changing the configuration files in `/backend` and the `vue.config.js`.
2. Set `ALLOWED_HOSTS` on [`backend.settings.prod`](/backend/settings/prod.py)
3. Follow the [Django deployment checklist](https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/) to make sure everything will work as expected from the back-end, changing the `.env` file as needed.

### 2.1 Local Deploy

After doing the changes above, follow the steps in [Running Development Servers](#1.3.%20Running%20Development%20Servers).

### 2.2 AWS Deploy

You can choose the topology you are most comfortable with:

Setting | Comment
--- | ---
EC2 single instance | recommended only for low and local traffic
EC2 Django + EC2 PostgreSQL + S3 for static files | good throughput
EC2 Django + EC2 PostgreSQL + CloudFront for static files | good throughput + locality
EC2 Django + RDS PostgreSQL + CloudFront for static files | highly scalable

As a Heroku alternative on AWS, check AWS Elastic Beanstalk.

### 2.3 Heroku Deploy

```sh
heroku apps:create iris-annotator
heroku git:remote --app iris-annotator
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DJANGO_SETTINGS_MODULE=backend.settings.prod
heroku config:set DJANGO_SECRET_KEY='< your django SECRET_KEY value >'

git push heroku
```

Heroku's nodejs buildpack will handle install for all the dependencies from the [`package.json`](/package.json) file. It will then trigger the `postinstall` command which calls `yarn build`. This will create the bundled `dist` folder which will be served by whitenoise. The python buildpack will detect the [`Pipfile`](/Pipfile) and install all the Python dependencies. The [`Procfile`](/Procfile) will run Django migrations and then launch Django's app using Gunicorn, as recommended by Heroku.

## 3. Management

### 3.1 CLI

```sh
./manage.py dbshell

# list databases
\l

# list tables
\d

# describe a table
\d api_annotation

# run a query - don't forget the semicolon:
SELECT id, annotator_id, image_id FROM api_annotation;

```

### 3.2 Dashboards

Feature | Default location | Comment
------- | ---------------- | -------
Django REST Framework | http://localhost:8000/api | Only available in development (_i.e._ `DEBUG=True`)
Django Administration Panel | http://localhost:8000/api/admin | Credentials created with `python manage.py createsuperuser`

### 3.3 Template Structure

| Location             |  Content                                   |
|----------------------|--------------------------------------------|
| `/backend`           | Django Project & Backend Config            |
| `/backend/api`       | Django App (`/api`)                        |
| `/src`               | Vue App .                                  |
| `/src/main.js`       | JS Application Entry Point                 |
| `/public/index.html` | HTML Application Entry Point (`/`)         |
| `/public/static`     | Static Assets                              |
| `/dist/`             | Bundled Assets Output (generated at `yarn build`) |
