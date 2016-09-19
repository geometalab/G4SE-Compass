FROM debian:jessie

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-dev \
      libxml2 libxml2-dev lib32z1-dev libxslt-dev libpq-dev libxslt1-dev\
      python3-pip python3-psycopg2 python3-lxml cron

RUN pip3 install sqlalchemy

ADD ./wait-for-it/wait-for-it.sh /bin/wait-for-it.sh

COPY ./docker-entrypoint.sh /bin/docker-entrypoint.sh

ADD ./src /src
ADD crontab /etc/cron.d/harvest-cron

RUN chmod 0644 /etc/cron.d/harvest-cron
RUN crontab /etc/cron.d/harvest-cron

ENTRYPOINT ["/bin/docker-entrypoint.sh"]
