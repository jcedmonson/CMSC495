#!/usr/bin/env zsh

echo "*** Creating Volumes ***"
docker volume create --name=auth_volume
docker volume create --name=data_volume

echo "*** Generating Certificates ***"

sudo rm -rf front-end/nginx/etc/nginx/ssl/
sudo mkdir front-end/nginx/etc/nginx/ssl/

openssl req -x509 -newkey rsa:4096 -keyout front-end/nginx/etc/nginx/ssl/key.pem -out front-end/nginx/etc/nginx/ssl/cert.pem -sha256 -days 365

echo "*** Creating Network ***"
docker network inspect cmsc495_network >/dev/null 2>&1 || \
    docker network create --driver bridge cmsc495_network

echo "*** Deploying ***"
docker compose -f docker-compose.yml up -d

docker compose logs

curl 127.0.0.1:8080

curl 127.0.0.1:4000
