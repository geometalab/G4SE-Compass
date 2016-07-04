FROM debian:jessie

RUN apt-get update && \
    apt-get install -y --no-install-recommends python python-dev \
      libxml2 libxml2-dev lib32z1-dev libxslt-dev libpq-dev libxslt1-dev\
      python-pip python-psycopg2 python-lxml cron

RUN pip install oaiharvest sqlalchemy

COPY ./docker-entrypoint.sh /

ADD ./src /src
ADD crontab /etc/cron.d/harvest-cron

RUN chmod 0644 /etc/cron.d/harvest-cron
RUN crontab /etc/cron.d/harvest-cron

ENTRYPOINT ["/docker-entrypoint.sh"]
