FROM mongo:latest

WORKDIR /data
COPY ./init-scripts /docker-entrypoint-initdb.d/

EXPOSE 27017

CMD ["mongod"]