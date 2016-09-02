# REST-API for G4SE
Developed using Django REST framework.

### Database
Database tables must be manually created using the database.sql script in an existing database.

### Testing
tbd.

### Docker
To run the image on production 3 environment variables must be set:
- DATABASE_URL: URL to the PostgreSQL
- DJANGO_SETTINGS_MODULE: "G4SE.production_settings" for production
- SECRET_KEY: secret key for the django application

Example(runs the API on port 8000):

sudo docker run -t -i -d --restart=always -p 127.0.0.1:8000:8000 -e DJANGO_SETTINGS_MODULE="G4SE.production_settings" -e DATABASE_URL=postgres://postgres:postgres@172.17.0.1:5432/G4SE -e SECRET_KEY=-ggz*k3ty+qhko8$nhw_b#p4e$3nlh5pzf^qeste=#j28 --name api geometalab/g4se-api