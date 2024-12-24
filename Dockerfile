FROM postgres:15.1

ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres \
    POSTGRES_DB=postgres

COPY init.sql /docker-entrypoint-initdb.d/