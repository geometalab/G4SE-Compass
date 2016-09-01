FROM python:3.5

RUN apt-get update && apt-get install -y \
		python3-psycopg2
ENV USER py

VOLUME /G4SE/staticfiles

ADD ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

ADD ./G4SE /G4SE
COPY ./docker-entrypoint.sh /


ENTRYPOINT ["/docker-entrypoint.sh"]