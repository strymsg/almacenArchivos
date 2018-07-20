'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
import os
import tempfile
import random

import pytest
from botadero import create_app
from botadero.shared import globalParams
from botadero.database import get_db

@pytest.fixture(scope='session')
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # create_app() tambien contiene inicializadores para la base de datos
    
    app = create_app(db_path=db_path, testing=True)
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
    yield get_db()

    
