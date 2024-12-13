#!/bin/bash

# Start Backend Server
cd backend-server || { echo "Failed to change directory to backend-server"; exit 1; }
make rm
make up
