"""
This file defines constants to be used in all configurations.

:copyright: (c) 2016 Pinn
:license: All rights reserved

"""

import os
import socket

hostname = os.environ.get('NODENAME', socket.gethostname())
# Use local hostname here, mine happpens to be ubuntu
if socket.gethostname() == 'ubuntu':
    hostname = socket.gethostname()

RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', '{}:5672'.format(hostname))
if RABBIT_HOSTNAME.startswith('tcp://'):
        RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

CELERY_BROKER_URL = 'amqp://{user}:{password}@{hostname}'.format(
    user=os.environ.get('RABBITMQ_DEFAULT_USER'),
    password=os.environ.get('RABBITMQ_DEFAULT_PASS'),
    hostname=RABBIT_HOSTNAME)
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TIMEZONE = 'America/Los_Angeles'
CELERY_ENABLE_UTC = True
CELERY_IGNORE_RESULTS = False
CELERY_TIME_LIMIT = 30

broker_url = CELERY_BROKER_URL
result_backend = CELERY_RESULT_BACKEND
timezone = CELERY_TIMEZONE
enable_utc = CELERY_ENABLE_UTC
ignore_results = CELERY_IGNORE_RESULTS
time_limit = CELERY_TIME_LIMIT
