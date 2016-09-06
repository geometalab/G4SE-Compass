#!/bin/bash
cd compass-frontend
npm install -g bower grunt
npm install
bower install
grunt build
cd ..
rm -rf nginx/g4se-frontend
cp -r compass-frontend/dist nginx/g4se-frontend
docker-compose build
