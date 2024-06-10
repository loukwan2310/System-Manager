#!/bin/sh

docker compose -f docker-compose.test.yml up -d --build
docker compose -f docker-compose.test.yml logs
docker exec csr_survey_test_django python manage.py test --keepdb
docker compose -f docker-compose.test.yml down
