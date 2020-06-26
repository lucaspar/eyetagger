#!/bin/bash

# LEAVE THIS AT THE PROJECT ROOT

pg_dump -h localhost -U annotator_admin annotation_tool | gzip > backend/dataset/annotations/db_backup_$(date +"%Y_%m_%d_%I_%M_%p").gz
if [ $? -eq 0 ]; then
   echo OK
else
   echo "Backup has failed."
fi
