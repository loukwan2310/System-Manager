ARG BUILD_TYPE=

FROM python:3.12.3-slim AS backendcore-base
RUN #rm -r /usr/local/lib/python3.12.3/ensurepip/
    # This is for #129953 and only applicable to Python3.9's image

#FROM backendcore-base AS backendcore-base-with-trustcert
## This is for avoid TLS error of ZScaler.
#ONBUILD COPY [ "Zscaler Root CA.pem", "/usr/local/share/ca-certificates/zscaler-ca-cert.crt" ]
#ONBUILD RUN apt-get update &&\
#    DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates &&\
#    update-ca-certificates &&\
#    DEBIAN_FRONTEND=noninteractive apt-get remove -y ca-certificates &&\
#    DEBIAN_FRONTEND=noninteractive apt-get -y autoremove &&\
#    DEBIAN_FRONTEND=noninteractive apt-get -y autoclean

# Force PIP & urllib3 to use system default trusted store
#ENV PIP_CERT /etc/ssl/certs/ca-certificates.crt
#ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt

FROM backendcore-base${BUILD_TYPE} as backendcore
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        libpq-dev \
        build-essential \
        gettext \
        poppler-utils \
        postgresql-client \
        graphviz \
        &&\
    DEBIAN_FRONTEND=noninteractive apt-get autoremove -y &&\
    DEBIAN_FRONTEND=noninteractive apt-get autoclean
RUN --mount=type=cache,target=/root/.cache \
    python -m pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt
#COPY /submodules /app/submodules
RUN #--mount=type=cache,target=/root/.cache \
#    /bin/sh -c 'cd ./submodules/kit_auth_aad; pip install -e .'

EXPOSE 8000 2222

RUN mkdir /app/files

RUN useradd -ms /bin/bash pyuser
USER pyuser

ARG VERSION_TAG
ENV VERSION_TAG=$VERSION_TAG


#################################################
### deploy images
#################################################

### base image for any deployment environment ###
FROM backendcore AS deploybase
USER pyuser
COPY --chown=pyuser:pyuser . /app
RUN django-admin compilemessages -l en -l ja

### image for system reset - deploy ###
FROM deploybase AS systemresetdeploy
ENV DJANGO_SETTINGS_MODULE=project.settings.deploy
CMD bash scripts/reset_system.sh

### image for database setup - deploy ###
FROM deploybase AS dbsetupdeploy
# ENV DJANGO_SETTINGS_MODULE=project.settings.deploy - Django code is not used in here
CMD bash scripts/start_dbsetup.sh

### image for database migration - deploy ###
FROM deploybase AS dbmigrationdeploy
ENV DJANGO_SETTINGS_MODULE=project.settings.deploy
CMD bash scripts/start_dbmigration.sh

### image for api container - deploy ###
FROM deploybase AS backenddeploy
ENV DJANGO_SETTINGS_MODULE=project.settings.deploy
CMD bash scripts/start_webapi.sh

### image for background task - deploy ###
FROM deploybase AS backgrounddeploy
ENV DJANGO_SETTINGS_MODULE=project.settings.noderunners
CMD bash scripts/start_background.sh noderunners.background


#################################################
### dev images
#################################################

### base image for any deployment environment ###
FROM backendcore AS devbase
USER root
COPY requirements-dev.txt /app
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements-dev.txt

COPY . /app
RUN django-admin compilemessages -l en -l ja
RUN #DJANGO_SECRET_KEY=DUMMY DJANGO_SETTINGS_MODULE=project.settings.dev bash kit_django/scripts/lint.sh
RUN #bandit -r .

### image for system reset - development environment ###
FROM devbase AS systemresetdev
ENV DJANGO_SETTINGS_MODULE=project.settings.dev
CMD rm -f /opt/system_reset_success &&\
    bash scripts/reset_system.sh &&\
    touch /opt/system_reset_success &&\
    sleep infinity

### image for database setup - development environment ###
FROM devbase AS dbsetupdev
# ENV DJANGO_SETTINGS_MODULE=project.settings.dev - Django code is not used in here
CMD rm -f /opt/dbsetup_success &&\
    bash scripts/start_dbsetup.sh &&\
    touch /opt/dbsetup_success &&\
    sleep infinity

### image for database migration - development environment ###
FROM devbase AS dbmigrationdev
ENV DJANGO_SETTINGS_MODULE=project.settings.dev
CMD rm -f /opt/dbmigration_success &&\
    bash scripts/start_dbmigration.sh &&\
    touch /opt/dbmigration_success &&\
    sleep infinity

### image for api container - development environment ###
FROM devbase AS backenddev
ENV DJANGO_SETTINGS_MODULE=project.settings.dev
CMD bash scripts/start_webapi.sh

#### image for background task - development environment ###
#FROM devbase AS backgrounddev
#ENV DJANGO_SETTINGS_MODULE=project.settings.dev_noderunners
#CMD watchmedo auto-restart --recursive --pattern=*.py -d ./noderunners/ -- bash scripts/start_background.sh noderunners.background
