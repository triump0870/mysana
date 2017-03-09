#!/bin/bash

if [ -n "$DATABASE_USER" ] && [ -n "$DATABASE_PASSWORD" ] && [ -n "$DATABASE_NAME" ]; then
	sed -e "s/{{DATABASE_NAME}}/$DATABASE_NAME/g" -e "s/{{DATABASE_USER}}/$DATABASE_USER/g"  -e "s/{{DATABASE_PASSWORD}}/$DATABASE_PASSWORD/" createdb.conf.template > /docker-entrypoint-initdb.d/entrypoint.sh
else
	echo "ERROR - Must specify: -e DATABASE_NAME, DATABASE_USER and DATABASE_PASSWORD"
	exit 1
fi

exec "$@"