# EyeTagger | Iris Annotation Tool

<img src="/src/assets/logo-iris.png" alt="Annotator Logo" width="50"/>

![](images/demo.png )

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

Data upload via web interface if not possible yet, so the data needs to be mounted inside the container.

If you have the images in the same machine, just put them in the expected location `data/dataset/` by creating a symbolic link (below) or just moving your data.

> `ln -s    $MY_DATASET_LOCATION    $(pwd)/data/dataset`

If your dataset is remote (cloud or another computer), you might want to start using `dvc`. Check the [Integrating DVC](#5.-integrating-dvc) session below.

### 1.3 Create environment

```sh
# copy all example dotenv files
sudo apt install mmv
mmv -c 'env/*.env.example' 'env/#1.env'

# edit all env/*.env files setting the following:
#    DJANGO_STATIC_HOST
#    SECRET_KEY
#    DB_PASS
#    POSTGRES_PASSWORD (same as DB_PASS)
find env -name "*.env" -exec nano {} \;
```

### 1.4. Run services

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

# access localhost:80 in your browser
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
Django REST Framework | http://localhost/api | Only available in development mode (_i.e._ `DEBUG=True` in `env/django_app.env`)
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

```txt
To run it every 6 hours:
0 */6 * * * /eyetagger/backups.sh >> /eyetagger/data/logs/backups.log 2>&1

Or every business day (Mon-Fri) at 6pm:
0 18 * * 1-5 /eyetagger/backups.sh >> /eyetagger/data/logs/backups.log 2>&1
```


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

1. There are 2 entries `command` under `docker-compose.yaml` > Service `web`. Select the "development" one by commenting our the other.

2. Run `docker-compose up` (run `down` first if already up) and open `localhost:9000`. Hot reload should be enabled i.e. live changes to the front-end code will update the browser.

## 4. Production Deploy

1. Adapt the environment files for the backend in `env/`.
2. Adapt the environment file for the frontend in `vue.config.js`.
3. Follow the [Django deployment checklist](https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/) for further configuration.
4. Deploy the dockerized application in a remote server by running it in daemon form: `docker-compose up -d && docker-compose logs -f`.

## 5. Integrating DVC

1. Install dvc on host

    > `pip install dvc`

2. Setup access (using a GCP below)

    ```sh
    # get provider-specific api
    pip install 'dvc[gs]'

    # create google bucket credentials
    mkdir -p $HOME/.gcp/
    GOOGLE_APPLICATION_CREDENTIALS=$HOME/.gcp/iris-admin.json

    # paste the contents of the GCP JSON in this file
    # see https://cloud.google.com/docs/authentication/getting-started"
    nano $GOOGLE_APPLICATION_CREDENTIALS
    chmod 400 $GOOGLE_APPLICATION_CREDENTIALS

    export GOOGLE_APPLICATION_CREDENTIALS
    echo -e ' >> Add this to your ~/.bashrc:\n\n\
        export GOOGLE_APPLICATION_CREDENTIALS='$GOOGLE_APPLICATION_CREDENTIALS'\n\n
    ```

3. Then get your data from the remote.

    > `dvc pull`

    Or add new data to the bucket

    > `dvc add data/dataset && dvc push`
