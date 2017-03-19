# The base image
FROM python:2.7

# Install all debian packages
RUN apt-get update && apt-get install -y \
        gcc \
        postgresql-client libpq-dev \
        python-dev \
        build-essential \
        vim \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN mkdir app-requirements/

COPY ./requirements.txt app-requirements/
COPY requirements app-requirements/requirements

RUN mkdir -p /var/log/app_logs

WORKDIR /app/
# install all the django dependencies
RUN pip install -r /app-requirements/requirements.txt

RUN pip install django-faker model_mommy
RUN pip install django-celery

RUN apt-get update && apt-get install -y \
    supervisor rabbitmq-server

EXPOSE 15672
EXPOSE 5672

COPY . /app/

RUN mkdir -p /var/log/celery
RUN mkdir -p /var/log/app_logs
RUN touch /var/log/celery/mysana_worker.log
RUN touch /var/log/celery/mysana_beat.log
RUN cp -f ./dockerify/uwsgi/celery_sup.conf /etc/supervisor/conf.d/
#RUN cp -f ./dockerify/uwsgi/celery_beat.conf /etc/supervisor/conf.d/

# Create the log directory for uwsgi and the shared directory for static files
RUN mkdir /var/log/uwsgi /shared

# Forward uwsgi logs to the docker log collector
RUN ln -sf /dev/stdout /var/log/uwsgi/djangoapp.log \
	&& ln -sf /dev/stdout /var/log/uwsgi/emperor.log


VOLUME /shared

# The port number on which the application will run
EXPOSE 30000

RUN chmod +x /app/dockerify/uwsgi/entrypoint.sh

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY:-'^141&epfu9xc1)ou_^qnx$uo4-z*n3a#s=d2lqutulog2o%!yu'}

RUN echo "export DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" >> ~/.bashrc

RUN echo "alias ll='ls -la'" >> ~/.bashrc

ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

ENTRYPOINT ["/app/dockerify/uwsgi/entrypoint.sh"]