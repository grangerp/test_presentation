#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

POWER_USER='vagrant'
SITE_NAME='test_presentation'
CONTAINER_PATH='/var/william'

apt-get update

apt-get -y install vim
apt-get -y install libpq-dev
apt-get -y install postgresql postgresql-client

apt-get -y install python-dev
apt-get -y install python-virtualenv
apt-get -y install libtiff-dev libjpeg-dev zlib1g-dev libfreetype6-dev

apt-get -y install gettext

apt-get -y install supervisor
apt-get -y install nginx


mkdir -p $CONTAINER_PATH
chown $POWER_USER:$POWER_USER $CONTAINER_PATH
sudo su postgres -c "psql -c \"CREATE USER $POWER_USER WITH ENCRYPTED PASSWORD '$POWER_USER' SUPERUSER;\""

# Fail, because the project was not yet deploy, but the link can already
# live without the source file.
ln -s $CONTAINER_PATH/$SITE_NAME/etc/supervisor.conf /etc/supervisor/conf.d/$SITE_NAME.conf
ln -s $CONTAINER_PATH/$SITE_NAME/etc/nginx.conf /etc/nginx/sites-available/$SITE_NAME
ln -s /etc/nginx/sites-available/$SITE_NAME /etc/nginx/sites-enabled/$SITE_NAME

nginx -s reload
supervisorctl reload