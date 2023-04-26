#!/usr/bin/env zsh

echo "*** Creating Volumes ***"
docker volume create --name=auth_volume
docker volume create --name=data_volume

echo "*** Generating Certificates ***"

CERTS_DIR=front-end/server/certs
rm -rf $CERTS_DIR
mkdir $CERTS_DIR

openssl req -x509 -newkey rsa:2048 -keyout $CERTS_DIR/keytmp.pem -out $CERTS_DIR/cert.pem -days 365
openssl rsa -in $CERTS_DIR/keytmp.pem -out $CERTS_DIR/key.pem

echo "*** Creating Network ***"
docker network inspect cmsc495_network >/dev/null 2>&1 || \
    docker network create --driver bridge cmsc495_network

echo "*** Deploying ***"
docker compose -f docker-compose.yml up -d

docker compose logs

curl 127.0.0.1:8080

curl 127.0.0.1:4000
