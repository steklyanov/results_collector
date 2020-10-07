#!/usr/bin/env bash
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn backend.wsgi -w 8 --max-requests 100 --max-requests-jitter 50 -b 0.0.0.0:8000
