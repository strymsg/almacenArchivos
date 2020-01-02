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
    assert len(nuevos1) > len(nuevos)
    os.remove(f1)

    nuevos2, borrados2, actualizados2 = sincronizarArchivos()
    assert len(nuevos2) < len(nuevos1)
    os.remove(f2)
    

# def test_sincronizarArchivosConFiltro(db):
#     from botadero.utils import addRelativeFileName
#     from botadero.database.models import Archivo
#     from botadero.controller import sincronizarArchivos
    
#     l1, l2 = sincronizarArchivos(['.gitignore'])
#     for filename in l1:
#         assert addRelativeFileName(filename) in l2
#     assert len(l1) == len(l2)

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
