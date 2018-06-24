''' 
El Botadero, una aplicación web para compartir archivos libremente.
Copyright (C) 2018 Rodrigo Garcia <strysg@riseup.net>
'''
from flask_sqlalchemy import SQLAlchemy

from flask import current_app as app

db = SQLAlchemy()

def init_db(app=None, db=None):
    ''' Re-Initializes database module.
    :param app: Flask instance app.
                If not providen flask.current_app is returned, if
                providen configures database object for the given app'''

    if app is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
        db = SQLAlchemy(app)

    print ('-------------- database object -------------')
    print (db)
    print ('-----------')
    return db
