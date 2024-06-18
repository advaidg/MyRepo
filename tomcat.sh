#!/bin/bash

# Ensure the credentials file exists
if [ ! -f /usr/local/tomcat/conf/db-credentials.properties ]; then
  echo "db-credentials.properties not found!"
  exit 1
fi

# Read credentials from the properties file
DB_USER=$(grep 'DB_USER' /usr/local/tomcat/conf/db-credentials.properties | cut -d '=' -f2)
DB_PASSWORD=$(grep 'DB_PASSWORD' /usr/local/tomcat/conf/db-credentials.properties | cut -d '=' -f2)

# Ensure the environment variables are set
if [ -z "$DB_USER" ]; then
  echo "DB_USER is not set in db-credentials.properties"
  exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
  echo "DB_PASSWORD is not set in db-credentials.properties"
  exit 1
fi

# Wait for the application to be unpacked
while [ ! -f /usr/local/tomcat/webapps/your-app/WEB-INF/classes/META-INF/context-template.xml ]; do
  sleep 1
done

# Replace placeholders in the context.xml file
sed -e "s/DB_USER_PLACEHOLDER/${DB_USER}/" \
    -e "s/DB_PASSWORD_PLACEHOLDER/${DB_PASSWORD}/" \
    /usr/local/tomcat/webapps/your-app/WEB-INF/classes/META-INF/context-template.xml > /usr/local/tomcat/webapps/your-app/WEB-INF/classes/META-INF/context.xml
