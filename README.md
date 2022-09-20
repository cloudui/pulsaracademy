# Pulsar Academy 🚀⭐

Pulsar Academy was an online code-teaching company that operated from 2020-2021. My friend Maxwell Zhang and I founded it during the COVID-19 pandemic in order to help students learn the fundamentals of coding and competitive programming. 

This website was made to streamline our project, as it handled the registration and payment process, class notes, and lecture videos (lessons were taught over call). It was also a good way to help me learn web development, as I was getting more familiar with Django and HTML/CSS/JS.

Now that I am in university, Pulsar Academy is no longer active, but this website remains a landmark to my progress with web development. I hope we were able to help our students find the joy in coding.

# Features 🛎😎
- User Registration and Login 
- Course registration, customizable profile, and password reset
    - Security via email confirmation via SendGrid SMTP Server
- Course payment via Paypal integration
- Customizable class with course schedule, lesson content via Markdown, embedded video, homework + solutions
- Rich course forum for students to communicate with one another

# Setup 🧑‍🍳

The whole project is containerized with Docker to streamline setup and execution.

1. You should download `docker` and `docker-compose`. Learn how to do that here: https://docs.docker.com/get-docker/.

2. Next, you should clone the repo using `git clone https://belowocean@bitbucket.org/belowocean/pythoncamp.git`.

## Local Deployment 💻

You can run the website locally using the `docker-compose.yml` file. The whole project will be set up after the images are downloaded and built.

```bash
$ docker-compose up -d --build
```

You need to migrate to the database before things will work:

```bash
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
```

Check `localhost:8000`or `127.0.0.1:8000` on your browser to check if it is working. 

## Production Deployment

You will need to shift over to the `docker-compose-prod.yml` or `docker-compose-test.yml` configuration file. This file uses more containers to be able to run the application.

### No HTTPS

Follows very similarly to above. First, you have to modify the NGINX configuration file located in `/config/nginx/local.conf/conf.d` and comment out the listener on port 443. You also need to comment out the line that does  automatic HTTPS forwarding and remove any reference to SSL within the listener on port 80. The configuration file should look something like this:

```nginx
upstream my_server {
    server web:80;
}
server {
    listen 80;
    server_name pulsaracademy.com;

    location / {
        proxy_pass http://my_server;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $Host;
        proxy_redirect off;
    }
    location /static/ {
        alias /code/staticfiles/;
        expires -1;
    }
}
```

This file is not included in the repo so you can just copy-paste it and replace the current `conf.d` file.

Next, you need to build the container and migrate to the database:

```bash
$ docker-compose -f docker-compose-test.yml up -d --build
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
```

Done!

### Yes HTTPS

Before building, you need to setup SSL certificates. I will assume the use of [Let's Encrypt](https://letsencrypt.org/) for SSL certification. This section assumes that you have a domain pointing to the IP or domain-name of whatever server you're using, otherwise it won't really work. For example, I had http://pulsaracademy.com pointing to `12.232.194` (example) before I ran the script described below.

A good guide you can follow is [this article by Medium user philipp](https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71), but I'll simplify it down here. 

The setup requires the SSL certificates to exist prior to building the container, so we will use a script to generate some dummy scripts first, which will eventually be replaced by real certificates. First, we should download the script and make it executable:

```bash
$ curl -L https://raw.githubusercontent.com/wmnnd/nginx-certbot/master/init-letsencrypt.sh > init-letsencrypt.sh
$ chmod +x init-letsencrypt.sh
```

First, you will need to change some fields in the file. You should enter the domains, name, and email into the appropriate fields in the file. Second, you will need to modify some commands in the script. All the `docker-compose` commands should be followed by `-f docker-compose-prod.yml`, otherwise the containers will fail. Another way to combat this is by renaming `docker-compose-prod.yml` to `docker-compose.yml`. Whichever one is better for you.

They should be in the first few lines of the script. Now, to run the script:

```bash
$ sudo ./init-letsencrypt.sh

# If that doesn't work, try this:
$ sudo bash init-letsencrypt.sh
```

If the process fails, maybe try building the docker-compose first, knowing it will fail. Or maybe try the non-HTTPS config first and come back. 

Assuming it worked, we can take down the containers and put them back up for self-assurance.

```bash
$ docker-compose -f docker-compose-prod.yml down
$ docker-compose -f docker-compose-prod.yml up -d
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
```

Enjoy! 

## A Note

Remember all the content on the website is technically copyrighted. This setup is just for you to see how it works or to help influence your own projects. Good luck!

# Technologies Employed

- Django
  - Python
  - HTML/CSS/JS
  - AJAX
- Docker
  - docker-compose
- NGINX
- PostgreSQL

