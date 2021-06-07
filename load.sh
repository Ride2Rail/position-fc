#!/bin/bash

# Start position-fc service
# docker-compose up -d

# Check if everything is up and running
sleep 5
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' http://127.0.0.1:5007/test)" != "200" ]]; do
	sleep 2
done

# Stop position-fc
#docker-compose down
