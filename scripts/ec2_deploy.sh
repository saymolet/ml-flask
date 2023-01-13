#!/usr/bin/env bash

# Obtain passed newest image name and export to use in docker-compose file
export IMAGE=$1
docker-compose -f docker-compose.yaml up --detach
echo "Success"