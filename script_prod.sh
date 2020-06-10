gunicorn pythoncamp_project.wsgi:application --bind 0.0.0.0:80
service cron start
printenv | grep -v "no_proxy" >> /etc/environment
python ./manage.py crontab add