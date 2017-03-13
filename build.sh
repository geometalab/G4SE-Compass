#!/bin/bash
pushd compass-frontend
rm -rf dist
ng build -prod
popd
docker-compose -f docker-build.yml build --pull
