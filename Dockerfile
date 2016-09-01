FROM nginx:alpine

COPY ./nginx.conf.template /etc/nginx/nginx.conf.template

COPY ./compass-frontend/dist /var/www/

CMD DOMAIN_NAMES=$(echo $VIRTUAL_HOST | sed 's/,/ /g') envsubst '$DOMAIN_NAMES' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf \
&& nginx -g 'daemon off;'