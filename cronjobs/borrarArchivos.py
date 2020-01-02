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
borrados = []
for categoria in categorias:
    borrados = co.comprobarTiempoBorradoListaArchivos(categoria)
    # se marca los templates para actualizarlos
    if len(borrados) > 0:
        co.marcarPaginaListaParaRenderizar(categoria=categoria)
    
print ('Sincronizando archivos...')
# sincronizando archivos y BD
archivos, archivosEnBd = u.sincronizarArchivos(ignorar=['gitkeep'])
print('archivos:\n', str(archivos), '\n', str(len(archivos)))
print('archivosEnBd:\n', str(archivosEnBd), '\n', str(len(archivosEnBd)))

# if len(archivos) != len(archivosEnBd):
    # aqui se debe reprocesar
    

print ('proceso borrado terminado')
sys.exit()
