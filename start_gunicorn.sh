nohup gunicorn app:app -c config.py -preload >gunicorn_log.log   2>&1 &
