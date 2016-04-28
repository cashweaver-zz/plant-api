#!/usr/bin/env bash
# Run the main app server

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Start the database
. $SCRIPT_DIR/mongod-start.sh

echo "Starting app"
node /home/vagrant/app/app.js
