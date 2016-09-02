# Dependencies
To deploy this project in production setup the harvester and api docker containers as described in their corresponding readme's.

# Nginx
The nginx container must be linked to the api container in order to publish its static files.

Additionaly the env variable VIRTUAL_HOST is required. In it you can set the sites domain name.

Example:

sudo docker run -t -i -d --link api:api --restart=always -p 0.0.0.0:80:80 --volumes-from api -e VIRTUAL_HOST="example.com" --name nginx geometalab/g4se-nginx
