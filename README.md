# EyeTagger | Iris Annotation Tool

<img src="/src/assets/logo-iris.png" alt="Annotator Logo" width="300"/>

## Summary

+ Dockerized application for simple deployment
+ PostgreSQL DB <=> Django + Gunicorn + Nginx web server <= REST API => Vue-based SPA + Vuex
+ Django Whitenoise to serve static files, CDN Ready
+ Annotations stored in relational database
+ Access control / user management
+ Vuex handles state management and persistance to never lose annotations on the front-end

## 1. Getting Started

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
docker-compose exec web pipenv run /app/manage.py migrate

# create django superuser
docker-compose exec web pipenv run /app/manage.py createsuperuser

# access localhost:8000 in your browser
```

---

## 2. Management

### 2.1 CLI access to services

#### Django + Vue container

> `docker-compose exec web /bin/bash`

#### Nginx container

> `docker-compose exec nginx /bin/sh`

#### PostgreSQL container

> `docker-compose exec db psql --username eyetagger_admin --dbname eyetagger`

More PostgreSQL commands:

```sh
\h  # help
\q  # quit
\l  # list databases
\d  # list tables / relations
\d api_annotation   # describe a table / relation

# run a query - don't forget the semicolon:
SELECT id, annotator_id, image_id FROM api_annotation;
```

### 2.2 Dashboards

Feature | Default location | Comment
------- | ---------------- | -------
Django REST Framework | http://localhost/api | Only available in development (_i.e._ `DEBUG=True` in `env/django_app.env`)
Django Administration Panel | http://localhost/api/admin | Credentials created with `pipenv run ./manage.py createsuperuser`

### 2.3 Template Structure

| Location from project root    | Contents                                  |
| ----------------------------- | ----------------------------------------- |
| `backend/`                    | Django Project & Backend Config           |
| `backend/api/`                | Django App for REST `api`                 |
| `data/`                       | Git-ignored: DB + backups                 |
| `deploy/`                     | Scripts and configuration files           |
| `dist/`                       | Git-ignored: back+front generated files   |
| `env/`                        | Environment Files                         |
| `public/`                     | Static Assets                             |
| `src/`                        | Vue App                                   |

### 2.4 Database

#### A. Backing up a DB (dump)

To run it once:

```sh
# docker-compose up db          # if db container is not running
docker-compose exec db pg_dump -U eyetagger_admin eyetagger | \
    gzip > eyetagger_bkp_$(date +"%Y_%m_%d_%I_%M_%p").sql.gz
```

Check [backups.sh](./backups.sh) for a simple automated version.

> Tip: you can add the existing `backups.sh` to your `crontab -e` for periodic backups:

    To run it every 6 hours:
    0 */6 * * * /eyetagger/backup.sh

    Or every business day (Mon-Fri) at 6pm:
    0 18 * * 1-5 /eyetagger/backup.sh


#### B. Restoring a Backup

```sh
# replace $YOUR_DUMP_GZ by your .gz location:

# let's copy the backup before moving/modifying it
cp $YOUR_DUMP_GZ /tmp/dump.sql.gz

# extract the dump
gunzip -k /tmp/dump.sql.gz

# copy to the running DB container
# docker-compose up db          # if db container is not running
docker cp /tmp/dump.sql eyetagger_db_1:/dump.sql

# create a new empty database
docker-compose exec db createdb -U eyetagger_admin -T template0 eyetagger_new

# populate the empty database with the dump
docker-compose exec db psql -U eyetagger_admin -d eyetagger_new -f /dump.sql

# swap database names
docker-compose exec db psql --username eyetagger_admin --dbname postgres
\l
ALTER DATABASE eyetagger RENAME TO eyetagger_old;
ALTER DATABASE eyetagger_new RENAME TO eyetagger;
\l
\q

# get the other services up and try it out!
docker-compose down && docker-compose up

# if successful, clean the temporary backup copies
rm      /tmp/dump.sql.gz     /tmp/dump.sql
```

## 3. Development

1. Run Vue development server

    > `docker-compose exec web yarn serve`

2. Open `localhost:8080`

## 4. Production Deploy

1. Adapt the environment files for the backend in `env/`.
2. Adapt the environment file for the frontend in `vue.config.js`.
3. Configure `ALLOWED_HOSTS` in [`backend.settings.prod`](/backend/settings/prod.py)
4. Follow the [Django deployment checklist](https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/) for further configuration.
5. Deploy the dockerized application in a remote server by running it in daemon form: `docker-compose up -d`.
