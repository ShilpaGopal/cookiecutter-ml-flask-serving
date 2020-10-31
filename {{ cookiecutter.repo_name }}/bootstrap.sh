#!/bin/bash

source /<SERVICE-NAME>/venv/bin/activate
gunicorn -c gunicorn.conf.py wsgi:service