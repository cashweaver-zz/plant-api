#!/usr/bin/env bash
# Download datasets from the NCDC

SAVE_PATH="/home/vagrant/plant-api/data/climatestations/raw"
mkdir -p "$SAVE_PATH"
cd "$SAVE_PATH"
if [[ "$(pwd)" != "$SAVE_PATH" ]]
then
  echo "Problem changing directory to $SAVE_PATH"
  exit 1;
fi
echo "Downloading datasets from the NCDC to $SAVE_PATH"

# Documentation
# ------------------------------------------------

WGET_OPTIONS="--no-verbose"

# README: Includes explanations on units, file naming, file structure, and more.
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt

# Methodology
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/documentation/temperature-methodology.pdf


# Data
# ------------------------------------------------

# Stations
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/station-inventories/allstations.txt
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/station-inventories/zipcodes-normals-stations.txt

# Temperature data
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/dly-tmax-normal.txt
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/dly-tmax-stddev.txt
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/dly-tmin-normal.txt
wget $WGET_OPTIONS http://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/dly-tmin-stddev.txt
