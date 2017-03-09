FROM postgres:9.5

RUN apt-get update && apt-get install -y \
    postgresql-9.5-postgis-2.2 postgresql-9.5-postgis-2.2-scripts

COPY ./dockerify/postgres/createdb.conf.template /app-postgres/createdb.conf.template
COPY ./dockerify/postgres/entrypoint.sh /app-postgres/entrypoint.sh

WORKDIR /app-postgres/

ARG DATABASE_USER
ENV DATABASE_USER ${DATABASE_USER}

ARG DATABASE_PASSWORD
ENV DATABASE_PASSWORD ${DATABASE_PASSWORD}

ARG DATABASE_NAME
ENV DATABASE_NAME ${DATABASE_NAME}

ARG PGPASSWORD
ENV PGPASSWORD=${PGPASSWORD}

RUN echo "export PGPASSWORD=$PGPASSWORD" >> ~/.bashrc
RUN echo "export DATABASE_USER=$DATABASE_USER" >> ~/.bashrc
RUN echo "export DATABASE_PASSWORD=$DATABASE_PASSWORD" >> ~/.bashrc
RUN echo "export DATABASE_NAME=$DATABASE_NAME" >> ~/.bashrc


RUN chmod +x entrypoint.sh
RUN ./entrypoint.sh

RUN chmod +x /docker-entrypoint-initdb.d/entrypoint.sh

# Port to use with TCP proxy
EXPOSE 5435
