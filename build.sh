#!/bin/bash
cd compass-frontend2
rm -rf dist
ng build -prod
docker-compose build
