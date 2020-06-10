printenv | grep -v "no_proxy" >> /etc/environment
service cron start
python ./manage.py crontab add
gunicorn pythoncamp_project.wsgi:application --bind 0.0.0.0:80