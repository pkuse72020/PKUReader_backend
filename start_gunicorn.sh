sudo nohup /home/se_gp7/.local/bin/gunicorn   app:app -c config.py -preload >gunicorn_log.log   2>&1 &
