#!/bin/bash
cd frontend
rm -rf dist
npm run build -p
docker-compose build
