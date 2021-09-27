docker-compose -f docker-compose-prod.yml down
docker-compose -f docker-compose-prod.yml up -d --build
docker-compose exec web python manage.py migrate
