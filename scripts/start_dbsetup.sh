#! /bin/bash
set -e

while ! pg_isready -h ${DB_HOST:-db} -p 5432 | grep -q 'accept'; do
  echo "Cannot connect to DB, retrying in 4 seconds..."
  sleep 4
done
echo "Database server is ready"

echo "Checking database status ..."
if [ "$( PGPASSWORD=${DB_PASS} psql -h ${DB_HOST:-db} -U ${DB_USER} -p 5432 -tAc "SELECT * FROM pg_database WHERE datname='${DB_NAME}';" template1 | wc -l )" == '1' ]
then
  echo "Database already exists"
else
  echo "Database does not exist"
  PGPASSWORD=${DB_PASS} psql -P "pager=off" -h ${DB_HOST} -U ${DB_USER} -p 5432 -c "CREATE DATABASE \"${DB_NAME}\";" template1
  PGPASSWORD=${DB_PASS} psql -P "pager=off" -h ${DB_HOST} -U ${DB_USER} -p 5432 -c "SELECT * FROM pg_database" template1
fi

if [ "$PRODUCTION" == "TRUE" ]
then

  echo "Create a new user"
  username=$DB_USER \
  password=$DB_PASS \
  bash scripts/create_postgres_user.sh

else
  # These users are only for docker-compose environment!
  
  echo "Create a new user for django"
  username=admin_manager \
  password=$DB_PASS \
  bash scripts/create_postgres_user.sh
#
#  echo "Create a new user for noderunner-background"
#  username=noderunnerbackground \
#  password=pass \
#  bash scripts/create_postgres_user.sh

fi