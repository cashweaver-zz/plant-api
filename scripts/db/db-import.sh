#!/usr/bin/env bash
# Import all data into the database

DATA_PATH='/home/vagrant/plant-api/data'

echo "Importing database"
echo "  plants"
mongoimport --drop --db plantapi --collection plants $DATA_PATH/plants.json
echo "  climatestations"
mongoimport --drop --db plantapi --collection climatestations $DATA_PATH/climatestations.json
