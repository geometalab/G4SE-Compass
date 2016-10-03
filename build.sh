#!/bin/bash
cd compass-frontend
rm -rf dist
ng build -prod
docker-compose build
