#!/usr/bin/env bash

DATA_PATH='/home/vagrant/plants-api/data'

echo "Importing database"
echo "  plants"
mongoimport --drop --db plantsapi --collection plants $DATA_PATH/plants.json
