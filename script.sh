
python /code/manage.py runserver 0.0.0.0:8000
service cron start
printenv | grep -v "no_proxy" >> /etc/environment
python /code/manage.py crontab add