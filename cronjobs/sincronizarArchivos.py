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
                
print ('proceso sincronizacion terminado')
sys.exit()
