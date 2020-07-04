#!/bin/bash

# parameters
DB_USER=eyetagger_admin
DB_NAME=eyetagger
BACKUP_NAME=eyetagger_bkp_$(date +"%Y_%m_%d_%I_%M_%p").sql.gz

# replace BACKUP_DIR value by the desired location
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BACKUP_DIR=$PROJECT_DIR/data/backups

# create backup location if it doesn't exist
mkdir -p $BACKUP_DIR

# dumps the SQL from database
docker exec eyetagger_db_1 pg_dump -U $DB_USER $DB_NAME | \
    gzip > $BACKUP_DIR/$BACKUP_NAME

# here you can also upload $BACKUP_DIR/$BACKUP_NAME
# somewhere else for a remote backup, (e.g. using dvc)
