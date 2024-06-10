Project
===

## Development environment
- OS: `Linux(Ubuntu 20.04)`
- IDE: `PyCharm(2023.1)`
- Language: `Python(3.9)`
- Framework: `Django(4.2)`
- Database: `Mysql(8)`
- Webserver: `Nginx(1.23.4)`
- Message broker: `Redis(redis:7-alpine)`
- Task queue system: `Celery(5.2.7)`
- Tools: `Docker(23.0.0)`, `docker-compose(v2.15.1)`


### Run the project in the development environment
1. Run `cp example.env  .env` and edit the values of the variables in the file according to.
   Example: 
   ```bash
        DJANGO_PORT=8080
        DJANGO_SECRET_KEY=5+$2ado9wtwb^gaf!mil%bt@8l$#qdbj!qw5fmy0c_on(
        WORKER=1
    
        DATABASE_NAME=db_dev
        DATABASE_USER=user_dev
        DATABASE_PASSWORD=password_dev
        DATABASE_ROOT_PASSWORD=root_password
        DATABASE_HOST=127.0.0.1
        DATABASE_PORT=3306
   
        REDIS_HOST=127.0.0.1
        REDIS_PORT=6379
        REDIS_PASSWORD=password
         
        CELERY_BROKER_URL=redis://:password@127.0.0.1:6379/0
        CELERY_RESULT_BACKEND=redis://:password@127.0.0.1:6379/0
   
        FIREBASE_ADMIN_CONFIG_PATH=app/firebase.json
   ```
2. Run the project using the docker 
   ```
   docker-compose -f docker-compose.yml up --build -d
   ```
3. To initialize user data, run the following command. By default, the command is run when using docker:
   ```bash
      python manage.py loaddata scripts/fixtures/admin_users.yaml
   ```
4. You can now visit the swagger interface at:       
- `http://host:port/api/swagger`
### Run the project in the production environment
1. Run `cp example.env  .env` and edit the values of the variables in the file according to.
   Example: 
   ```bash
        DJANGO_PORT=8080
        DJANGO_SECRET_KEY=5+$2ado9wtwb^gaf!mil%bt@8l$#qdbj!qw5fmy0c_on(
        WORKER=1
    
        DATABASE_NAME=db_production
        DATABASE_USER=user_prod
        DATABASE_PASSWORD=password_prod
        DATABASE_ROOT_PASSWORD=root_password
        DATABASE_HOST=127.0.0.1
        DATABASE_PORT=3306
   
        REDIS_HOST=127.0.0.1
        REDIS_PORT=6379
        REDIS_PASSWORD=password
         
        CELERY_BROKER_URL=redis://:password@127.0.0.1:6379/0
        CELERY_RESULT_BACKEND=redis://:password@127.0.0.1:6379/0
   
        FIREBASE_ADMIN_CONFIG_PATH=app/firebase.json
   ```
2. Run the project using the docker 
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```
   Note: Production environment hides swagger link
3. To initialize user data, run the following command. By default, the command is run when using docker:
   ```bash
      python manage.py loaddata scripts/fixtures/admin_users.yaml
   ```

### Run the project in the test environment

1. Run `cp example.env  .env` and edit the values of the variables in the file according to. 
   Example: 
   ```bash
        DJANGO_PORT=8080
        DJANGO_SECRET_KEY=5+$2ado9wtwb^gaf!mil%bt@8l$#qdbj!qw5fmy0c_on(
        WORKER=1
    
        DATABASE_NAME=db_test
        DATABASE_USER=user_test
        DATABASE_PASSWORD=password_test
        DATABASE_ROOT_PASSWORD=root_password
        DATABASE_HOST=127.0.0.1
        DATABASE_PORT=3306
   
        REDIS_HOST=127.0.0.1
        REDIS_PORT=6379
        REDIS_PASSWORD=password
         
        CELERY_BROKER_URL=redis://:password@127.0.0.1:6379/0
        CELERY_RESULT_BACKEND=redis://:password@127.0.0.1:6379/0
   
        FIREBASE_ADMIN_CONFIG_PATH=app/firebase.json
   ```
2. Run the project using the docker `docker-compose -f docker-compose.test.yml up --build -d`
3. Run `docker exec webapi-test python manage.py test --keepdb`

## Project structure
```bash
.
├── api
│   ├── v1
│   │   └── urls.py
│   │   └── __init__.py
│   ├── v2
│   │   ├── urls.py
│   │   └── __init__.py
│   └── __init__.py
├── apps #A mother-folder containing all apps for our project. An app can be a django template project
│   └── example_app 
│       ├── api
│       │   ├── __init__.py
│       │   │   serializers.py
│       │   │   urls.py
│       │   │   views.py
│       │   └── 
│       ├── management
│       │   ├── commands
│       │   │   └── command.py
│       │   └── __init__.py
│       ├── migrations
│       │   └── __init__.py
│       ├── templates
│       ├── tests
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
├── common # An optional folder containing common "stuff" for the entire project
│   ├── __init__.py
├── docs
│   ├── CHANGELOG.md
├── locale
│   ├── en
│   ├── ja
├── project
│   ├── settings
│   │   ├── __init__.py
│   │   │── deploy.py
│   │   └── dev.py
│   ├── asgi.py
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── docs
│   ├── CHANGELOG.md
├── scripts
│   ├── code_scanning.sh
│   ├── start_webapi.sh
├── .coveragerc
├── .dockerignore
├── .flake8
├── .gitignore
├── .pylintrc
├── docker-compose.prod.yml
├── docker-compose.test.yml
├── docker-compose.yml
├── Dockerfile
├── example.env
├── manage.py
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## Usage

| period      | command                                                               | description              |
|-------------|-----------------------------------------------------------------------|--------------------------|
| development | `python manage.py makemigration`                                      | Create migrations        |
| development | `python manage.py migrate`                                            | Migrate Database         |
| development | `python manage.py compilemessages -l en -l ja`                        | Internationalization     |
| development | `python manage.py runserver`                                          | Start server development |
| production  | `gunicorn --bind 0.0.0.0:${port} -k gevent -w ${worker} project.wsgi` | Start server production  | 
