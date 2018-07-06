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
from botadero import utils

# NOTA: para ver los mensajes en print usar: pytest -s

# def test_config():
#     assert not create_app()
#     assert create_app({'TESTING': true}).testing

def test_listaDeArchivos():
    lista = utils.listaDeArchivos()
    print ('lista obtenida:')
    for l in lista:
        print (l)
    assert len(lista) > 0

def test_hashArchivo_sinAceleracion():
    archivo = os.path.join(globalParams.uploadDirectory, '.gitkeep')
    hexdigest = utils.hashArchivo(archivo)
    print ('hash sin aceleracion', hexdigest)
    assert hexdigest == 'd901cf70a95e546dbfedb749c40b6932f03a8e6f'

def test_hashArchivo_conAceleracion():
    archivo = os.path.join(globalParams.uploadDirectory, '.gitkeep')
    hexdigest = utils.hashArchivo(archivo, accelerateHash=True)
    print ('hash con aceleracion', hexdigest)
    assert hexdigest != 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
