#!/bin/bash
export TAG=$1
docker-compose -f /home/ubuntu/app/docker-compose.yaml down
docker-compose -f /home/ubuntu/app/docker-compose.yaml up -d
