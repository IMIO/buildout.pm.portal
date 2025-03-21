#!/usr/bin/dumb-init /bin/bash
set -e
COMMANDS="debug help logtail show stop adduser fg kill quit run wait console foreground logreopen reload shell status"
START="start restart zeoserver"
CMD="bin/instance"

python3 /docker-initialize.py
mkdir -p /data/{log,filestorage,blobstorage}

if [ "$CRON" = "True" ]; then
  echo "Setting up the cron task"
  echo -e "machine localhost\nlogin admin\npassword $ADMIN_PASSWORD" > ./.netrc
  chmod 600 ./.netrc
  touch /data/log/cron.log
  service cron start
  (crontab -u imio -l 2>/dev/null ; echo "*/15 * * * * curl -s -m 10 --netrc-file /plone/.netrc http://localhost:8081/$SITE_ID/@@tick_fifteen >> /data/log/cron.log 2>&1 && echo '' >> /data/log/cron.log") | crontab -
fi

if [ -e "custom.cfg" ]; then
	if [ ! -e "bin/develop" ]; then
		buildout -c custom.cfg
		python3 /docker-initialize.py
	fi
fi

if [[ "$1" == "zeo"* ]]; then
	CMD="bin/$1"
fi

if [ -z "$HEALTH_CHECK_TIMEOUT" ]; then
	HEALTH_CHECK_TIMEOUT=1
fi

if [ -z "$HEALTH_CHECK_INTERVAL" ]; then
	HEALTH_CHECK_INTERVAL=1
fi

if [[ $START == *"$1"* ]]; then
	_stop() {
		$CMD stop
		kill -TERM "$child" 2>/dev/null
	}

	trap _stop SIGTERM SIGINT
	$CMD start
	$CMD logtail &
	child=$!

	pid=$($CMD status | sed 's/[^0-9]*//g')
	if [ -n "$pid" ]; then
		echo "Application running on pid=$pid"
		sleep "$HEALTH_CHECK_TIMEOUT"
		while kill -0 "$pid" 2>/dev/null; do
			sleep "$HEALTH_CHECK_INTERVAL"
		done
	else
		echo "Application didn't start normally. Shutting down!"
		_stop
	fi
else
	if [[ $COMMANDS == *"$1"* ]]; then
		exec bin/instance "$@"
	fi
	exec "$@"
fi
