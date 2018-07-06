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

@pytest.fixture
def app():
    app = create_app({
        'TESTING': true
    })

    # agregar aqui inicializadores de base de datos
    # ...

    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
