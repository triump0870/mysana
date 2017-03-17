#!/bin/bash

set -e

if [ "$DEBUG" == "True" ]; then
	# check if the postgres service is up before starting django migration
    until psql -h "$DATABASE_HOST" -U "$PGUSER"  -c '\l'; do
      >&2 echo "Postgres is unavailable - sleeping"
      sleep 5
    done

    >&2 echo "Postgres is up - executing command"
fi

echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config
rabbitmq-plugins enable rabbitmq_management
/etc/init.d/rabbitmq-server restart
/etc/init.d/supervisor restart

echo yes | python src/manage.py migrate
echo yes | python src/manage.py collectstatic --noinput

supervisorctl update
supervisorctl status mysanacelery
supervisorctl status mysanacelerybeat

# Forward app logs to docker log collector
tail -n0 -F /var/log/app_logs/*.log &
tail -n0 -F /var/log/celery/*.log &
tail -n0 -F /var/log/supervisor/supervisord.log &

# start uwsgi
exec uwsgi --emperor dockerify/uwsgi/ --gid www-data

