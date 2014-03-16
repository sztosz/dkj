#!/bin/bash
LOGFILE=/_dev/logs/dkj-test/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
USER=root
GROUP=root
ADDRESS=sztosz.tk:8888
source /_dev/dkj-test-venv/bin/activate
cd /_dev/www/dkj-test/dkj/dkj
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS --bind=$ADDRESS \
	--user=$USER --group=$GROUP --log-level=debug \
	--log-file=$LOGFILE 2>>$LOGFILE dkj.wsgi:application
