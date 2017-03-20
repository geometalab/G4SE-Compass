FROM python:3.5

RUN apt-get update && apt-get install -y python3-psycopg2 libev-dev

ENV USER py

ADD ./wait-for-it/wait-for-it.sh /bin/wait-for-it.sh
ADD ./dev-requirements.txt /dev-requirements.txt
RUN pip3 install -r /dev-requirements.txt

ADD ./G4SE /G4SE
COPY ./docker-entrypoint.sh /bin/docker-entrypoint.sh
COPY ./wait_only_docker-entrypoint.sh /bin/wait_only_docker-entrypoint.sh
COPY ./uwsgi_docker.ini /uwsgi.ini

ENV STATIC_URL /api/static/
ENV STATIC_ROOT /var/data/static
ENV MEDIA_URL /api/media/
ENV MEDIA_ROOT /var/data/media

VOLUME /var/data

ENTRYPOINT ["/bin/docker-entrypoint.sh"]

CMD uwsgi /uwsgi.ini --processes ${NUM_PROCESSES:-2} --threads ${NUM_THREADS:-1}
