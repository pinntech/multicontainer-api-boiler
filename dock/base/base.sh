#!/bin/bash

# Supervisor
chmod 777 /etc/supervisor/supervisord.conf

# Permissions
#############
#echo "supervisor ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
mkdir -p /var/log/uwsgi
chmod -R +rw /var/log/supervisor
chmod -R +rw /var/log/uwsgi
chmod -R 777 /var/www/app
