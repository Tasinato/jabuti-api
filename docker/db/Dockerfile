# docker/db/Dockerfile
FROM postgres:16-alpine

# Scripts em /docker-entrypoint-initdb.d rodam automaticamente
# na primeira inicialização (quando o volume ainda está vazio).
COPY ./docker/db/init.sql /docker-entrypoint-initdb.d/001-init.sql