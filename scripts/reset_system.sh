#!/bin/sh
set -e

if [ "$CONFIRM_TO_RESET" != "OperateReset" ]
then
    echo "Cannot operate reset command."
    exit 1
fi

echo "Clean up database:"
python manage.py flush --no-input

echo "Reconfigure database records:"
python manage.py loaddata apps/users/fixtures/*.yaml
python manage.py loaddata scripts/fixtures/admin-user.json

echo "Reset Azure Blob Storage:"
export PYTHONPATH="$PYTHONPATH:/app/common/"
python scripts/cleanup_storage.py

echo "Done"
