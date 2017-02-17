FROM  nginx:alpine
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
# Copy built app to wwwroot
COPY index.html /usr/share/nginx/html/index.html
COPY dist /usr/share/nginx/html/dist
