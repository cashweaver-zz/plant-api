#!/usr/bin/env bash
# Build data required for db initialization

DATA_PATH="/home/vagrant/plant-api/data"

echo "Creating $DATA_PATH"
mkdir "$SAVE_PATH"

echo "Building plantapi.plants"
# There's nothing to do at the moment.
# Plant data doesn't need building.

echo "Building plantapi.climatestations"
