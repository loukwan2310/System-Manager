#! /bin/sh
set -e

# Alias psql exec command
sql_command()
{
  PGPASSWORD=$DB_PASS psql -P "pager=off" -U $DB_USER -h ${DB_HOST} -p 5432 -d ${DB_NAME} -c "$@"
}

set_all()
{
  sql_command "GRANT ALL ON ALL TABLES IN SCHEMA public TO $username;"
  sql_command "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO $username;"
  sql_command "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO $username;"
  sql_command "GRANT ALL ON SCHEMA public TO $username;"
  sql_command "GRANT ALL ON DATABASE \"${DB_NAME}\" TO $username;"
}

set_permissions()
{
  local TABLES_CRUD=$1
  local TABLES_CRU=$2
  local TABLES_R=$3
  local TABLES_RU=$4
  local TABLES_CR=$5
  local TABLES_SEQ=$6
  local TABLES_RD=$7

  echo "CURD = $TABLES_CRUD"
  echo "CURD = $TABLES_CRU"
  echo "R = $TABLES_R"
  echo "RU = $TABLES_RU"
  echo "CR = $TABLES_CR"
  echo "SEQ = $TABLES_SEQ"
  echo "RD = $TABLES_RD"

  # Revoke existing permissions from user;
  sql_command "REVOKE ALL ON ALL TABLES IN SCHEMA public FROM $username;"
  sql_command "REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM $username;"
  sql_command "REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM $username;"
  sql_command "REVOKE ALL ON SCHEMA public FROM $username;"
  sql_command "REVOKE ALL ON DATABASE \"${DB_NAME}\" FROM $username;"
  # Allow to use `public`
  sql_command "GRANT USAGE ON SCHEMA public TO $username;"
  # Revoke default prividedge
  sql_command "GRANT $username TO current_user;"
  sql_command "ALTER DEFAULT PRIVILEGES FOR ROLE $username IN SCHEMA public REVOKE ALL ON TABLES FROM $username;"
  sql_command "ALTER DEFAULT PRIVILEGES FOR ROLE $username IN SCHEMA public REVOKE ALL ON SEQUENCES FROM $username;"

  [ "$TABLES_CRUD" != "" ] && sql_command "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE $TABLES_CRUD TO $username;" # tables CRUD
  [ "$TABLES_CRU"  != "" ] && sql_command "GRANT SELECT, INSERT, UPDATE         ON TABLE $TABLES_CRU  TO $username;" # tables CRUD
  [ "$TABLES_R"    != "" ] && sql_command "GRANT SELECT                         ON TABLE $TABLES_R    TO $username;" # tables _R__
  [ "$TABLES_RU"   != "" ] && sql_command "GRANT SELECT,         UPDATE         ON TABLE $TABLES_RU   TO $username;" # tables _RU_
  [ "$TABLES_CR"   != "" ] && sql_command "GRANT SELECT, INSERT                 ON TABLE $TABLES_CR   TO $username;" # tables CR__
  [ "$TABLES_SEQ"  != "" ] && sql_command "GRANT SELECT, USAGE                  ON TABLE $TABLES_SEQ  TO $username;" # tables sequence
  [ "$TABLES_RD"   != "" ] && sql_command "GRANT SELECT, DELETE                 ON TABLE $TABLES_RD   TO $username;" # tables _R_D

}

show_permissions()
{
  sql_command "
    SELECT grantee
      ,table_catalog
      ,table_schema
      ,table_name
      ,string_agg(privilege_type, ', ' ORDER BY privilege_type) AS privileges
      FROM information_schema.role_table_grants
      WHERE grantee = '$username'
      GROUP BY grantee, table_catalog, table_schema, table_name
      ;"
}

# === CREATE/UPDATE USER ===
if [ -z "$username" ]; then
  echo "username is empty, Exiting..."
  exit 1;
fi
echo "User name = $username"

while ! pg_isready -h ${DB_HOST} -p 5432 | grep -q 'accept'; do
  echo "Cannot connect to DB, retrying in 4 seconds..."
  sleep 4
done

echo "DB Ready, Start creating..."


# If username is existing, update password
if [ -z "$password" ]; then
  echo "password is empty, skip password config..."
elif sql_command "SELECT 1 FROM pg_roles WHERE rolname='$username';" | grep -q '1'; then
  sql_command "ALTER USER $username WITH PASSWORD '$password';"
  echo "User $username already exists, updating password."
else
  sql_command "CREATE USER $username WITH PASSWORD '$password' NOSUPERUSER;"
  echo "Created $username and set password."
fi

### === GRANT PERMISSIONS ===
if [ -z "$permission" ]; then
  echo "No 'permission' parameter is passed, skipping..."
elif [ "$permission" == "all" ]; then
  set_all
  show_permissions
  echo "Granted all privileges to user: $username"
elif [ "$permission" == "webapi" ]; then

  TABLES_CRUD="
    auth_group,
    auth_group_permissions,
    auth_permission,
    users_users
  "
  TABLES_CRU="
  django_session
  "
  TABLES_R="
    django_content_type,
    django_migrations
  "
  TABLES_RD="
    django_admin_log
  "
  TABLES_RU=""
  TABLES_CR="
  django_session
  "
  TABLES_SEQ="
    auth_group_id_seq,
    auth_group_permissions_id_seq,
    auth_permission_id_seq,
    django_admin_log_id_seq,
    django_content_type_id_seq,
    django_migrations_id_seq
  "
  set_permissions "$TABLES_CRUD" "$TABLES_CRU" "$TABLES_R" "$TABLES_RU" "$TABLES_CR" "$TABLES_SEQ" "$TABLES_RD"
  show_permissions
  echo "Granted permission to user: $username"
else
  echo "Permission should be one of: [all, webapi]"
fi
