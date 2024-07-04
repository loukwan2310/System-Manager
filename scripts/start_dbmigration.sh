#! /bin/bash
set -e

while ! pg_isready -h ${DBHOST:-db} -p 5432 | grep -q 'accept'; do
  echo "Cannot connect to DB, retrying in 4 seconds..."
  sleep 4
done
echo "Database server is ready"

echo "Database Migrating..."
#python manage.py migrate
#python manage.py loaddata apps/users/fixtures/*.yaml
#python manage.py init_permission_master
#python manage.py populate_history --auto

# Create users
echo "-----"
echo ${DBUSER_WEBAPI:-55555555}
echo "-----"
echo "Set permissions of django/admin_manager"
username=${DBUSER_WEBAPI:-admin_manager} \
permission=webapi \
bash scripts/create_postgres_user.sh

#echo "Set permissions of noderunnerbackground"
#username=${DBUSER_NODERUNNER_BACKGROUND:-noderunnerbackground} \
#permission=noderunner-background \
#bash scripts/create_postgres_user.sh
