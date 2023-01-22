FROM mysql:8.0.31

ENV MYSQL_ROOT_PASSWORD admin
ENV MYSQL_DATABASE notesdb

COPY create_table.sql /docker-entrypoint-initdb.d/

EXPOSE 3306