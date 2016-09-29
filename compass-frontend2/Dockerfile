FROM node:4

RUN npm install -g live-server

ENV PORT=3000

EXPOSE $PORT

ADD dist /var/data/www/compass

WORKDIR /var/data/www/compass

CMD live-server --entry-file=/index.html --host=0.0.0.0 --port=$PORT --no-browser

