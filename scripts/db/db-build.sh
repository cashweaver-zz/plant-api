#!/usr/bin/env bash
# Build data required for db initialization

BASE_PATH="/home/vagrant/plant-api"
DATA_PATH="$BASE_PATH/data"

echo "Creating $DATA_PATH"
mkdir "$SAVE_PATH"

echo "Building plantapi.plants"
# There's nothing to do at the moment.
# Plant data doesn't need building.

echo "Building plantapi.climatestations"
. $BASE_PATH/scripts/db/climatestations/climatestaions-download.sh
python $BASE_PATH/scripts/db/climatestations/climatestaions-process.py
