'''
This file is part of "El Botadero"
copy
right 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
from flask_sqlalchemy import SQLAlchemy
from flask import g, current_app
from flask_sqlalchemy import BaseQuery

def setup_db(app, db=None, destroy=True, db_path='sqlite:///db.sqlite3', testing=False):
    ''' Re-Initializes database module.
    :param app: Flask instance app.
    :param destroy: If True forces drop all tables then create again
    '''
    if testing:
        if not db_path.startswith('sqlite:///'):
            db_path = 'sqlite:///' + db_path
            
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #from .models import db
    db = SQLAlchemy(app)
    db.init_app(app)

    if destroy:
        db.drop_all()
    g.db = db
    # importando modelos definidos en modulos externos
    print ('Importando modelos ... ')
    from .models import Archivo
    
    db.create_all()
    db.session.commit()
    # Archivo.create(name='prueba1.py', extension='py')
    # Archivo.create(name='prueba2.py', extension='py')
    # print('Archivo.query.all():', str(Archivo.query.all()))
    print ('Base de datos creada!', str(app.config['SQLALCHEMY_DATABASE_URI']), '>>>', str(db))

    return g.db

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    return g.db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
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
        return db.session.commit()
