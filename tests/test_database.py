import os
import tempfile

import pytest
import uuid
from flask import current_app
from botadero.shared import globalParams
from botadero.database import get_db

# def test_get_close_db(db):
#     with current_app.app_context():
#         db = get_db()
#         assert db is get_db()

def test_crearArchivo(db):
    from botadero.database.models import Archivo
    name = uuid.uuid4().hex
    a = Archivo.create(name=name, extension='')
    assert Archivo.query.filter_by(name=name) is not None

def test_eliminarArchivo(db):
    from botadero.database.models import Archivo
    name = uuid.uuid4().hex
    a = Archivo.create(name=name, extension='py')
    a.delete()
    l = Archivo.query.filter_by(name=name).all()
    assert len(l) == 0
    
def test_listarArchivo(db):
    from botadero.database.models import Archivo
    name = uuid.uuid4().hex
    a = Archivo.create(name=name, extension='')
    assert Archivo.query.filter_by(name=name).first() is not None
    
def test_modificarArchivo(db):
    from botadero.database.models import Archivo
    name = uuid.uuid4().hex
    b = Archivo.create(name=name, extension='')
    assert Archivo.query.filter_by(name=name).first() is not None
    name = uuid.uuid4().hex
    b.save(name=name)
    assert Archivo.query.filter_by(name=name).first() is not None

# tabla html_pages
def test_crearHtmlPage(db):
    from botadero.database.models import HtmlPage
    name = uuid.uuid4().hex
    b = HtmlPage.create(name=name, category='Misc')
    assert HtmlPage.query.filter_by(name=name).first() is not None

