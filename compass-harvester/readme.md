# G4SE metadata harvesting service
This container periodically harvests medatadata from a G4SE compliant OAI-PMH data provider and writes the results into a specified PostgreSQL database.

### Docker commands
#### Build image:
docker build  --rm -t g4se-harvester .

#### Run container:
There are 3 enviroment Variables all of which are required to successfully run the container:
- DATA_PROVIDER_URL: Base URL for the OAI data provider
- DATABASE_URL: URL to the PostgreSQL database with port, username and password. If the database is on the host dont use localhost but the ip of the docker network interface (found with sudo ip addr show docker0)
- METADATA_FORMAT: OAI metadata format (probably G4SE) 

Example:
- sudo docker run -t -i -d --name harvester -e DATA_PROVIDER_URL=https://g4sedataprovider.ch/oai2 -e DATABASE_URL=postgres:postgres@172.17.0.1:5432/G4SE -e METADATA_FORMAT=G4SE g4se-harvester

