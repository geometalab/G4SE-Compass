#!/bin/bash
cd compass-frontend
grunt clean
grunt build
cd ..
rm -rf nginx/g4se-frontend
cp -r compass-frontend/dist nginx/g4se-frontend
docker-compose build
