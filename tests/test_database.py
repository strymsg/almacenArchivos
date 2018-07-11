import os
import tempfile

import pytest
from botadero.shared import globalParams
from botadero.database.models import Archivo
from botadero.database import get_db

def test_crearArchivo(app):
    Archivo.create(name='test.py', extension='py')
    Archivo.create(name='test2.py', extension='py')
    #a1 = Archivo(name='test.py', extension='py')
    #a2 = Archivo(name='prueba.py', extension='py')
    #a1.save()
    #a2.save()
    
    # db = get_db()
    # print (':::: Db', str(db))
    # db.session.add(a1)
    # db.session.add(a2)
    # db.session.commit()

    print ('Archivo.query.all():', str(Archivo.query.all()))
    assert Archivo.query.filter_by(name='test.py') is not None
    assert Archivo.query.filter_by(name='prueba.py') is not None
