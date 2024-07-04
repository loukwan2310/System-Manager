#! /bin/bash
set -e

while ! pg_isready -h ${DB_HOST:-db} -p 5432 | grep -q 'accept'; do
  echo "Cannot connect to DB, retrying in 4 seconds..."
  sleep 4
done
echo "DB Ready, Starting $1..."

while true; do
  SHOW_MIGRATIONS=$(python manage.py showmigrations)
  if [ $(echo "$SHOW_MIGRATIONS" | grep '\[ \]' | wc -l) != "0" ]
    then
      echo "Some migration(s) are pending." 1>&2
      echo "$SHOW_MIGRATIONS" 1>&2
      sleep 4
    else
      break
    fi
done

python manage.py noderunner $1
