#!/bin/bash

# Start Web Dashboard
cd dashboard || { echo "Failed to change directory to dashboard"; exit 1; }
yarn start
