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

/etc/init.d/celeryd start

python src/manage.py migrate
yes | python src/manage.py collectstatic --noinput

# Forward app logs to docker log collector
tail -n0 -F /var/log/app_logs/*.log &

# start uwsgi
exec uwsgi --emperor dockerify/uwsgi/ --gid www-data

