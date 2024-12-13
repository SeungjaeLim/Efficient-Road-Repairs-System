#!/bin/bash

# Start GS1 EPCIS V2.1.2
cd epcisV2/v2_1_2 || { echo "Failed to change directory to epcisV2/v2_1_2"; exit 1; }
docker-compose up
