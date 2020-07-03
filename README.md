# EyeTagger | Iris Annotation Tool

<img src="/src/assets/logo-iris.png" alt="Annotator Logo" width="300"/>

## Summary

+ Dockerized application for simple deployment
+ PostgreSQL DB <=> Django + Gunicorn + Nginx web server <= REST API => Vue-based SPA + Vuex
+ Django Whitenoise to serve static files, CDN Ready
+ Annotations stored in relational database
+ Access control / user management
+ Vuex handles state management and persistance to never lose annotations on the front-end

## 1. Execution

### 1.1. Dependencies

Before getting started you should have the following installed and running:

+ Docker >= v19
+ Docker Compose >= v1.25

### 1.2. Link data

To pass the images you want to be served with the EyeTagger, open `docker-compose.yaml` and edit the volume entries commented with `dataset`. Set their `source` fields to point to the directory containing the images.

To make things easier when deploying remotely, you can [make use of `dvc`](https://dvc.org/) on your dataset and run commands such as `dvc push` and `dvc pull` to sync the data between a number of machines and a remote (e.g. AWS S3, Google Cloud Storage); similarly to what `git` does with source code.

### 1.3. Setup Template

#### Install Packages

```sh
# create the public network
docker network create net-nginx-proxy

# build docker images and run containers
docker-compose up

# from another terminal, run the database migrations
docker exec -it eyetagger_web_1 pipenv run /app/manage.py migrate

# create django superuser
docker exec -it eyetagger_web_1 pipenv run /app/manage.py createsuperuser

# access localhost:8000 in your browser
```

## 2. Deploy

1. Adapt the environment files for the backend in `env/`.
2. Adapt the environment file for the frontend in `vue.config.js`.
3. Configure `ALLOWED_HOSTS` in [`backend.settings.prod`](/backend/settings/prod.py)
4. Follow the [Django deployment checklist](https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/) for further configuration.
5. Deploy the dockerized application in a remote server by running it in daemon form: `docker-compose up -d`.

## 3. Management

### 3.1 CLI

Gain CLI access to app container

> `docker exec -it eyetagger_web_1 /bin/bash`

Gain

```sh
docker exec -it eyetagger_db_1 psql --username eyetagger_admin --dbname eyetagger

# list databases
\l

# list tables
\d

# describe a table (relation)
\d api_annotation

# run a query - don't forget the semicolon:
SELECT id, annotator_id, image_id FROM api_annotation;

```

### 3.2 Dashboards

Feature | Default location | Comment
------- | ---------------- | -------
Django REST Framework | http://localhost:8000/api | Only available in development (_i.e._ `DEBUG=True` in `env/django_app.env`)
Django Administration Panel | http://localhost:8000/api/admin | Credentials created with `pipenv run ./manage.py createsuperuser`

### 3.3 Template Structure

| Location from project root    | Contents                                  |
| ----------------------------- | ----------------------------------------- |
| `backend`                     | Django Project & Backend Config           |
| `backend/api`                 | Django App (`/api`)                       |
| `dist/`                       | Bundled Assets Output (backend + frontend)|
| `env/`                        | Backend environment files                 |
| `public/index.html`           | HTML Application Entry Point (`/`)        |
| `public/static`               | Static Assets                             |
| `src`                         | Vue App .                                 |
| `src/main.js`                 | JS Application Entry Point                |
