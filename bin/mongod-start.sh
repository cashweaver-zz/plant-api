#!/usr/bin/env bash
# Start mongod if it isn't already running.

if [[ ! $(ps -eadf | grep "[m]ongod") ]]; then
  echo "Starting mongod"
  mongod &
fi
