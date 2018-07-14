import os
import tempfile

import pytest
import uuid
from flask import current_app
from botadero.shared import globalParams
from botadero.database import get_db

# def test_get_close_db(app):
#     with current_app.app_context():
#         db = get_db()
#         assert db is get_db()

def test_crearArchivo(db):
    from botadero.database.models import Archivo
    name = uuid.uuid4().hex
    a = Archivo.create(name=name, extension='')
    assert Archivo.query.filter_by(name=name) is not None

def test_listarArchivo(db):
    from botadero.database.models import Archivo
    l = Archivo.query.filter_by(name='test.py').all()
    print('LISTA:',str(l))
    assert len(l) > 0
    
def test_modificarArchivo(db):
    from botadero.database.models import Archivo
    a = Archivo.query.filter_by(name='test.py').first()
    a.save(name='Nuevo')
    assert a.name == 'Nuevo'

def test_eliminarArchivo(db):
    from botadero.database.models import Archivo
    name = uuid.uuid4().hex
    a = Archivo.create(name=name, extension='py')
    a.delete()
    l = Archivo.query.filter_by(name=name).all()
    assert len(l) == 0
    
