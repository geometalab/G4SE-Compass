FROM nginx:alpine

COPY ./nginx.conf.template /etc/nginx/conf.d/default.conf.template

COPY ./g4se-frontend /var/www/g4se-frontend

CMD DOMAIN_NAMES=$(echo $VIRTUAL_HOST | sed 's/,/ /g') envsubst '$DOMAIN_NAMES' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf \
    && nginx -g 'daemon off;'
