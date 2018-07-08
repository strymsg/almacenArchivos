''' 
El Botadero, una aplicación web para compartir archivos libremente.
Copyright (C) 2018 Rodrigo Garcia <strysg@riseup.net>
'''
from flask import current_app, g

db = None

def setup_db(app, db=None, destroy=True):
    ''' Re-Initializes database module.
    :param app: Flask instance app.
    :param destroy: If True forces drop all tables then create again
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .models import db
    db.init_app(app)

    if destroy:
        db.drop_all()

    # importando modelos definidos en modulos externos
    print ('Importando modelos ... ')
    from . import Archivo
    db.create_all()
    db.session.commit()
        
    archivo = Archivo(name='prueba.py', extension='py')
    print (archivo)
    db.session.add(archivo)
    db.session.commit()
    g.db = db
    print('Archivo.query.all():', str(Archivo.query.all()))

    return g.db

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # if 'db' not in g:
    #     with app.app_context():
    #         g.db = init_db(current_app)
    return g.db
