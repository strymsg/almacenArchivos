''' 
El Botadero, una aplicación web para compartir archivos libremente.
Copyright (C) 2018 Rodrigo Garcia <strysg@riseup.net>
'''
from flask_sqlalchemy import SQLAlchemy
from . import models

from flask import current_app as app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///db.sqlite3'
db = SQLAlchemy(app)

def init_db(app=None):
    ''' Re-Initializes database module.
    :param app: Flask instance app.
                If not providen flask.current_app is returned, if
                providen configures database object for the given app'''

    if app is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///db.sqlite3'
        db = SQLAlchemy(app)

    return db
