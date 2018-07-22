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
from flask import current_app
# NOTA: para ver los mensajes en print usar: pytest -s

def test_listaDeArchivos():
    from botadero.utils import listaDeArchivos

    lista = listaDeArchivos()
    print ('lista obtenida:')
    for l in lista:
        print (l)
    assert len(lista) > 0

def test_hashArchivo_sinAceleracion():
    from botadero.utils import hashArchivo

    archivo = os.path.join(globalParams.uploadDirectory, '.gitkeep')
    hexdigest = hashArchivo(archivo)
    print ('hash sin aceleracion', hexdigest)
    assert hexdigest == 'd901cf70a95e546dbfedb749c40b6932f03a8e6f'

def test_hashArchivo_conAceleracion():
    from botadero.utils import hashArchivo

    #nombreYRuta = crearArchivoPrueba(4918800)
    archivo = os.path.join(globalParams.uploadDirectory, '.gitkeep')
    hexdigest = hashArchivo(archivo, accelerateHash=True)
    print ('hash con aceleracion', hexdigest)
    assert hexdigest != 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

def test_registrarArchivo(db):
    from botadero.utils import registrarArchivo
    from botadero.database.models import Archivo
    
    nombreYRuta = crearArchivoPrueba()
    registrado = registrarArchivo(nombreYRuta)
    print ('ARchivo registrado:', str(registrado))
    assert registrado is not None
    assert Archivo.query.filter_by(name=registrado.name).first() is not None

def test_existeArchivoEnBD(db):
    from botadero.utils import existeArchivo, registrarArchivo
    from botadero.database.models import Archivo

    nombreYRuta = crearArchivoPrueba()
    registrado = registrarArchivo(nombreYRuta)
    assert existeArchivo(nombreYRuta) is not None
    nombreYRuta = crearArchivoPrueba()
    assert existeArchivo(nombreYRuta) is None

def test_borrarArchivo(db):
    from botadero.utils import existeArchivo, registrarArchivo, borrarArchivo
    from botadero.database.models import Archivo

    nombreYRuta = crearArchivoPrueba()
    registrado = registrarArchivo(nombreYRuta)
    assert existeArchivo(nombreYRuta) is not None
    assert borrarArchivo(nombreYRuta) is True
    assert existeArchivo(nombreYRuta) is None

def test_sincronizarArchivos(db):
    from botadero.utils import sincronizarArchivos, addRelativeFileName
    from botadero.database.models import Archivo

    l1, l2 = sincronizarArchivos()
    for filename in l1:
        assert addRelativeFileName(filename) in l2
    assert len(l1) == len(l2)

def test_sincronizarArchivosConFiltro(db):
    from botadero.utils import sincronizarArchivos, addRelativeFileName
    from botadero.database.models import Archivo
    
    l1, l2 = sincronizarArchivos(['.gitignore'])
    for filename in l1:
        assert addRelativeFileName(filename) in l2
    assert len(l1) == len(l2)
    
# utils para pruebas
def crearArchivoPrueba(numCadenas=5000):
    db_fd, db_path = tempfile.mkstemp(suffix='.txt')
    
    with open(db_path, 'w') as file:
        i = int(numCadenas)
        cont = ''
        while i > 10:
            cont += ',' + str(random.randint(1,i))
            i -= 1
        file.write(cont)
    return db_path
