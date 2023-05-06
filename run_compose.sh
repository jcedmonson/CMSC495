#!/usr/bin/env zsh
docker volume create --name=data_volume

docker network inspect cmsc495_network >/dev/null 2>&1 || \
    docker network create --driver bridge cmsc495_network


run_full_clean=0
display_help=0

while getopts :hf flag
do
    case "${flag}" in
        f) run_full_clean=1;;
        h) display_help=1;;
    esac
done

if [ $display_help -gt 0 ]
  then
    echo "Use -f the completely rebuild the containers and remove any orphans. Without any flags, the normal stand up will be used"
    exit
  fi

if [ $run_full_clean -gt 0 ]
then
  docker compose -f docker-compose.yml up -d --force-recreate --build --remove-orphans
else
  docker compose -f docker-compose.yml up -d
fi

docker compose logs

curl 127.0.0.1:8080

curl 127.0.0.1:4000
