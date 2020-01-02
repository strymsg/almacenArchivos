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
    from botadero.utils import listaDeArchivos, categorias

    # categorias
    try:
        listaCategorias = categorias()
        for categoria in listaCategorias:
            lista = listaDeArchivos(categoria)
            print ('lista obtenida:', str(lista))
            for l in lista:
                print (l)
            #assert len(lista) > 0
    except:
        print ('Error listando archivos')
        assert 1 == 0

def test_hashArchivo_sinAceleracion():
    from botadero.utils import hashArchivo

    archivo = os.path.join(os.path.abspath(os.curdir),
                           'tests', 'fixtures', 'archivos', '1.txt')
    hexdigest = hashArchivo(archivo)
    print ('hash sin aceleracion 1.txt', hexdigest)
    assert hexdigest == '6e07f20f10664b06c50faa52dd5fad44d0e4461d'
    
    archivo = os.path.join(os.path.abspath(os.curdir),
                           'tests', 'fixtures', 'archivos', 'pingüino.jpg')
    hexdigest = hashArchivo(archivo) 
    print ('hash sin aceleracion pingüino.jpg', hexdigest)
    assert hexdigest == 'dce3c92b190dfd3a4a3d82b31f360ded041dcdfa'

    # archivo grande
    archivo = os.path.join(os.path.abspath(os.curdir),
                           'tests', 'fixtures', 'archivos',
                           'pasto1.jpg')
    hexdigest = hashArchivo(archivo)
    print ('hash sin aceleracion pasto1.jpg', hexdigest)
    assert hexdigest == '1da479d184c1cf9a7d8df498c842ab258912a482'

def test_hashArchivo_conAceleracion():
    from botadero.utils import hashArchivo

    # archivo chico
    archivo = os.path.join(os.path.abspath(os.curdir),
                           'tests', 'fixtures', 'archivos', '1.txt')
    hexdigest = hashArchivo(archivo, accelerateHash=True)
    print ('hash con aceleracion 1.txt', hexdigest)
    assert hexdigest == '6e07f20f10664b06c50faa52dd5fad44d0e4461d'
    # archivo mediano
    archivo = os.path.join(os.path.abspath(os.curdir),
                           'tests', 'fixtures', 'archivos', 'pingüino.jpg')
    hexdigest = hashArchivo(archivo, accelerateHash=True)
    print ('hash con aceleracion pingüino.jpg', hexdigest)
    assert hexdigest == 'dce3c92b190dfd3a4a3d82b31f360ded041dcdfa'

    # archivo grande
    archivo = os.path.join(os.path.abspath(os.curdir),
                           'tests', 'fixtures', 'archivos',
                           'pasto1.jpg')
    hexdigest = hashArchivo(archivo, accelerateHash=True)
    print ('hash con aceleracion pasto.jpg', hexdigest)
    assert hexdigest == '04433af3f8541ea34903e6e3cbda075a953cd6f2'
    

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

def test_descargarAchivo(db):
    from botadero.utils import descargarArchivo, registrarArchivo
    from botadero.database.models import Archivo

    nombreYRuta = crearArchivoPrueba()
    registrado = registrarArchivo(nombreYRuta)
    assert descargarArchivo(cat='', nombreArchivo=nombreYRuta) is not None
    a = Archivo.query.filter_by(path=nombreYRuta).first()
    assert a.downloads == 1

# @pytest.fixture
# def test_crearHtmlListado_forzado(db):
#     #flaskr.app.config['TESTING'] = True
#     print ('listadoooooooooooooooo')
#     from botadero.database.models import HtmlPage
#     from botadero.utils import crearHtmlListado, sincronizarArchivos
#     l1, l2 = sincronizarArchivos()
#     html_page = crearHtmlListado(categoria='Misc', force=True)
#     assert flask.request.path == '/'
#     assert flask.request.args['name'] == 'Peter'
#     #flaskr_app.config['SERVER_NAME'] = 'local'
#     print('------------------------html---------')
#     print ('test_crearHtmlListado_forzado:', str(html_page))
#     assert html_page is not None

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
