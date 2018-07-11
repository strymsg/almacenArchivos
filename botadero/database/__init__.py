'''
This file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
print('__init.py<database>')

from flask_sqlalchemy import SQLAlchemy
from flask import g
from flask import current_app
from flask_sqlalchemy import BaseQuery

#from .database import setup_db, db, get_db
# from .models import Archivo
# from .models import CRUDMixin

#db = SQLAlchemy()
#print('db(1):', str(db))

def setup_db(app, db=None, destroy=True, db_path='sqlite:///db.sqlite3'):
    ''' Re-Initializes database module.
    :param app: Flask instance app.
    :param destroy: If True forces drop all tables then create again
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #from .models import db
    db = SQLAlchemy(app)
    print('db(setup_db):', str(db))
    db.init_app(app)

    if destroy:
        db.drop_all()

    g.db = db
    
    # importando modelos definidos en modulos externos
    print ('Importando modelos ... ')
    from .models import Archivo
    
    db.create_all()
    db.session.commit()
        
    #archivo = Archivo(name='prueba.py', extension='py')
    Archivo.create(name='prueba1.py', extension='py')
    Archivo.create(name='prueba2.py', extension='py')
    #print (archivo)
    #db.session.add(archivo)
    #db.session.commit()
    print('Archivo.query.all():', str(Archivo.query.all()))

    return g.db

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    return g.db
    # with current_app.app_context():
    #     return g.db

class CRUDMixin(object):

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def save(self):
        """Saves the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete the object from the database."""
        db.session.delete(self)
        db.session.commit()
        return self


