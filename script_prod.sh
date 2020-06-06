service cron start
printenv | grep -v "no_proxy" >> /etc/environment
python /code/manage.py crontab add