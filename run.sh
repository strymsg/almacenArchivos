#!/bin/sh
# ejecuta la aplicacion con uwsgi
VENV=venv

export FLASK_ENV=production
export FLASK_APP=botadero.py

$VENV/bin/uwsgi --ini app.ini

