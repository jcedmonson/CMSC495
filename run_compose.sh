#!/usr/bin/env zsh
docker volume create --name=data_volume

docker network inspect cmsc495_network >/dev/null 2>&1 || \
    docker network create --driver bridge cmsc495_network

# Use this for normal start up
#docker compose -f docker-compose.yml up -d

# use this for a complete cleanup
docker compose -f docker-compose.yml up -d --force-recreate --build --remove-orphans

docker compose logs

curl 127.0.0.1:8080

curl 127.0.0.1:4000
