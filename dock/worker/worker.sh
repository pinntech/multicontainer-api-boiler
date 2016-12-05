#!/bin/bash

# Wait on broker initialization
sleep 5

export PYTHONUSERBASE=".venv"
source .env

log=/usr/src/worker/log/worker.log
pid=/usr/src/worker/log/worker.pid
touch $log
touch $pid

celery worker -A dock.worker.tasks.celery -l info --uid=celery
