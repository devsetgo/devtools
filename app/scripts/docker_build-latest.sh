#!/bin/bash
set -e
set -x

# cat /home/mike/twitter-star/app/scripts/docker_token.txt | docker login docker.pkg.github.com -u devsetgo --password-stdin

IMAGE_NAME="twitterstar"
IMAGE_VERSION=$(TZ=America/New_York date +"%y-%m-%d")

docker build -t docker.pkg.github.com/devsetgo/twitter_star/$IMAGE_NAME:$IMAGE_VERSION .
docker push docker.pkg.github.com/devsetgo/twitter_star/$IMAGE_NAME:$IMAGE_VERSION
docker build -t docker.pkg.github.com/devsetgo/twitter_star/$IMAGE_NAME:latest .
docker push docker.pkg.github.com/devsetgo/twitter_star/$IMAGE_NAME:latest