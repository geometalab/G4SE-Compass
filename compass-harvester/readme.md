# G4SE metadata harvesting service
This container periodically harvests data from a share containing xml file using a csv index on the share

### Docker commands
#### Build image:
docker build  --rm -t geometalab/g4se-harvester .

#### Run container:
There are 2 enviroment Variables all of which are required to successfully run the container:
- DATABASE_URL: URL to the PostgreSQL database with port, username and password. If the database is on the host dont use localhost but the ip of the docker network interface (found with sudo ip addr show docker0)
- FILESHARE_URL: URL to the fileshare root containing xml files and a csv index

Example:
`docker run -t -i -d --restart=always --name harvester -e DATABASE_URL=postgres:postgres@172.17.0.1:5432/G4SE -e FILESHARE_URL=https://geodata4edu.ethz.ch/metadata/ geometalab/g4se-harvester`
