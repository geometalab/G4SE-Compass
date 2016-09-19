FROM python:3.5

RUN apt-get update && apt-get install -y python3-psycopg2

ENV USER py

ADD ./wait-for-it/wait-for-it.sh /bin/wait-for-it.sh
ADD ./dev-requirements.txt /var/data/G4SE/dev-requirements.txt
RUN pip3 install -r /var/data/G4SE/dev-requirements.txt

ADD ./G4SE /G4SE
COPY ./docker-entrypoint.sh /bin/docker-entrypoint.sh

ENTRYPOINT ["/bin/docker-entrypoint.sh"]

CMD /usr/local/bin/gunicorn G4SE.wsgi:application --bind 0.0.0.0:8000
