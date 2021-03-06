'''
this file is part of "El Botadero"
copyright 2019 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
import os
import tempfile
import random

import pytest
from botadero import create_app
from botadero import shared
from flask import current_app

# NOTA: para ver los mensajes en print usar: pytest -s

def test_sincronizarArchivos(db):
    from botadero.utils import addRelativeFileName
    from botadero.database.models import Archivo
    from botadero.controller import sincronizarArchivos

    nuevos, borrados, actualizados = sincronizarArchivos()

    f1 = crearArchivoPrueba(dir=shared.globalParams.uploadDirectory)
    f2 = crearArchivoPrueba(dir=shared.globalParams.uploadDirectory)
    print('temporales creados:')
    print(f1)
    print(f2)
    nuevos1, borrados1, actualizados1 = sincronizarArchivos()
    assert len(nuevos1) > 0
    os.remove(f1)

    nuevos2, borrados2, actualizados2 = sincronizarArchivos()
    assert len(borrados2) > 0
    os.remove(f2)

def test_descargarArchivoProtegido():
    from botadero.utils import hashPassword, registrarArchivo, comprobarPassword, borrarArchivo, existeArchivo, descargarArchivo
    from botadero.controller import descargarArchivo
    
    nombreYRuta = crearArchivoPrueba()
    hashedPassword = hashPassword('123456')
    registrado = registrarArchivo(nombreYRuta, hashedPassword=hashedPassword)
    assert not isinstance(descargarArchivo('', nombreYRuta, password='123456'), dict)
    assert borrarArchivo(nombreYRuta) is True
    assert existeArchivo(nombreYRuta) is None

def test_descargarArchivoProtegidoError():
    from botadero.utils import hashPassword, registrarArchivo, comprobarPassword, borrarArchivo, existeArchivo, descargarArchivo
    from botadero.controller import descargarArchivo
    
    nombreYRuta = crearArchivoPrueba()
    hashedPassword = hashPassword('123456')
    registrado = registrarArchivo(nombreYRuta, hashedPassword=hashedPassword)
    assert isinstance(descargarArchivo('', nombreYRuta, password='12vawe'), dict) is True
    assert borrarArchivo(nombreYRuta) is True
    assert existeArchivo(nombreYRuta) is None
    
# def test_subirArchivo(db):
#     from botadero.controller import subirArchivo
#     from botadero.utils import nombreArchivo, borrarArchivo, existeArchivo

#     db_fd, db_path = tempfile.mkstemp(suffix='.txt', dir=shared.globalParams.uploadDirectory)
#     with open(db_path, 'w') as file:
#         i = 5000
#         cont = ''
#         while i > 10:
#             cont += ',' + str(random.randint(1,i))
#             i -= 1
#         file.write(cont)
#         resp = subirArchivo('', file, '123456')
#         assert 'tipoError' not in resp
#         assert existeArchivo(db_path) is not None
#     assert borrarArchivo(db_path) is True

# utils para pruebas
def crearArchivoPrueba(numCadenas=5000, dir=None):
    db_fd, db_path = tempfile.mkstemp(suffix='.txt', dir=dir)
    
    with open(db_path, 'w') as file:
        i = int(numCadenas)
        cont = ''
        while i > 10:
            cont += ',' + str(random.randint(1,i))
            i -= 1
        file.write(cont)
    return db_path


