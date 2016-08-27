#!/usr/bin/env bash

DATA_PATH='/home/vagrant/plant-api/data'

echo "Importing database"
echo "  plants"
mongoimport --drop --db plantapi --collection plants $DATA_PATH/plants.json
