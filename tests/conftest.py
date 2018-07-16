'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
import os
import tempfile

import pytest
from botadero import create_app
from botadero.shared import globalParams
from botadero.database import get_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    print ('>>>>', db_path)
    
    # create_app() tambien contiene inicializadores para la base de datos
    
    app = create_app(db_path=db_path, testing=True)
    # app = create_app({
    #     'TESTING': true,
    #     'DATABASE': db_path,
    # })
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def db(app):
    # ctx = app.app_context()
    # ctx.push()
    # yield get_db()
    #from botadero.database.models import Archivo
    yield get_db()
    #yield get_db()
