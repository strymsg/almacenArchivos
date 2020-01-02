'''
this file is part of "El Botadero"
copyright 2019 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
# Este script se encarga de comprobar el tiempo de los archivos y si es necesario borrarlos del sistema de archivos y de la base de datos

# Tambien se encarga de sincronizar los archivos registrados en la BD y los existentes en el sitema de archivos, al hacer esta sincronizacion si se detectan cambios se marca la tabla `html_pages' en la BD para que se vuelvan a renderizar las paginas html con jinja2.

import os
import sys

from botadero.shared import globalParams, gr
from botadero import controller as co

# comprobando tiempo borrado
co.sincronizarArchivos(ignorar=['.gitkeep', '.gitkeep~', '#.gitkeep', '#.gitkeep#'])

# categorias = u.categorias()
# categorias.append('Misc')

# print ('Comprobando tiempo de borrado de archivos...')
# borrados = []
# for categoria in categorias:
#     borrados = co.comprobarTiempoBorradoListaArchivos(categoria)
#     # se marca los templates para actualizarlos
#     if len(borrados) > 0:
#         co.marcarPaginaListaParaRenderizar(categoria=categoria)
    
# # sincronizando archivos y BD
# lsArchivos, registrosEnBd = u.sincronizarArchivos(ignorar=['gitkeep'])
# archivosEnBd = []
# archivos = []

# for reg in registrosEnBd:
#     archivosEnBd.append(reg.path)

# for archivo in lsArchivos:
#     archivos.append(os.path.join(os.path.curdir + os.path.sep, archivo))
    
# print('archivos:\n', str(archivos), '\n', str(len(archivos)))
# print('archivosEnBd:\n', str(archivosEnBd), '\n', str(len(archivosEnBd)))

# if len(archivos) != len(archivosEnBd):
#     # aqui se debe rerprocesar

#     # caso nuevos archivos en el sistema de archivos
#     if len(archivos) > len(archivosEnBd):
#         for archivo in archivos:
#             if archivo not in archivosEnBd:
#                 print ('+', str(archivo))
#                 # agrega y marca nueva pagina para renderizar
#                 co.marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivo))
#     else:
#         # caso archivos que han sido borrados del sistema de archivos
#         for archivoEnBd in archivosEnBd:
#             if archivoEnBd not in archivos:
#                 # agrega y marca nueva pagina para renderizar
#                 print('-', str(archivoEnBd))
#                 co.marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivoEnBd))
#                 # borra registro en la BD
#                 u.borrarRegistroArchivoEnBd(u.nombreArchivo(archivoEnBd))
                
print ('proceso sincronizacion terminado')
sys.exit()
