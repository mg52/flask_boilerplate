#!/bin/sh

gunicorn --chdir app wsgi:app --workers=3 --worker-class=gevent --worker-connections=1000 -b 0.0.0.0:8003
