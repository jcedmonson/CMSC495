#!/usr/bin/env zsh
docker volume create --name=data_volume

docker network inspect cmsc495_network >/dev/null 2>&1 || \
    docker network create --driver bridge cmsc495_network

docker compose -f docker-compose.yml up -d

docker compose logs

curl 127.0.0.1:8080

curl 127.0.0.1:4000
