docker-compose -f docker-compose-prod.yml down
docker-compose -f docker-compose-prod.yml up -d
docker-compose exec web python manage.py migrate
