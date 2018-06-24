''' 
El Botadero, una aplicación web para compartir archivos libremente.
Copyright (C) 2018 Rodrigo Garcia <strysg@riseup.net>
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app=None, db=None, destroy=True):
    ''' Re-Initializes database module.
    :param app: Flask instance app.
                If not providen flask.current_app is returned, if
                providen configures database object for the given app'''

    if app is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
        db = SQLAlchemy(app)

    if destroy:
        print ('db.create_all')
        db.drop_all()
        db.create_all()
        
    return db
