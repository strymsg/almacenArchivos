'''
this file is part of "El Botadero"
copyright 2019 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
# Este script se encarga de comprobar el tiempo de los archivos y si es necesario borrarlos del sistema de archivos y de la base de datos

import os
import sys

from botadero.shared import globalParams, gr
from botadero import utils as u
from botadero import controller as co

# comprobando tiempo borrado
categorias = u.categorias()
categorias.append('Misc')
print ('Comprobando tiempo de borrado de archivos...')
for categoria in categorias:
    co.comprobarTiempoBorradoListaArchivos(categoria)

print ('Sincronizando archivos...')
# sincronizando archivos y BD
u.sincronizarArchivos(ignorar=['gitkeep'])

print ('proceso borrado terminado')
sys.exit()
