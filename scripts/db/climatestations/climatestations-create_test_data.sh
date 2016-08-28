#!/usr/bin/env bash
# Download datasets from the NCDC

DATA_PATH="/home/vagrant/plant-api/data/climatestations/raw"
cd "$DATA_PATH"
if [[ "$(pwd)" != "$DATA_PATH" ]]
then
  echo "Problem changing directory to $DATA_PATH"
  exit 1;
fi

# Stations
head -n2 allstations.txt | tail -n1 > allstations-test.txt
# Average
head -n12 dly-tavg-normal.txt > dly-tavg-normal-test.txt
head -n12 dly-tavg-stddev.txt > dly-tavg-stddev-test.txt
# Minimum
head -n12 dly-tmax-normal.txt > dly-tmax-normal-test.txt
head -n12 dly-tmax-stddev.txt > dly-tmax-stddev-test.txt
# Maximum
head -n12 dly-tmin-normal.txt > dly-tmin-normal-test.txt
head -n12 dly-tmin-stddev.txt > dly-tmin-stddev-test.txt
