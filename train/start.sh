#!/bin/bash

celery --app=train.tasks.celery worker -Q station,speed --loglevel=info -E &&
celery beat --app=train.tasks.celery --loglevel=info