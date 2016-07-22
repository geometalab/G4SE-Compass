FROM python:3.5

RUN apt-get update && apt-get install -y \
		python3-psycopg2
ENV USER py

ENV HOME /home/$USER

WORKDIR $HOME

ADD ./requirements.txt $HOME/requirements.txt
RUN pip3 install -r requirements.txt

ADD ./G4SE $HOME/G4SE
COPY ./docker-entrypoint.sh $HOME


ENTRYPOINT ["/home/py/docker-entrypoint.sh"]