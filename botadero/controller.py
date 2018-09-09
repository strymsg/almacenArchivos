'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
# El objetivo de este archivo es albergar la logica compleja del botadero
import os

from .shared import globalParams, gr
from . import utils as u
from .database.models import Archivo

def descargaPermitida(cat, nombreArchivo):
    if '..' in nombreArchivo or nombreArchivo.startswith(os.path.sep):
        return False
    if cat not in u.categorias() and cat != 'Misc':
        return False
    return True

def descargarArchivo(cat, nombreArchivo):
    # agregar descargar de utils
    pathf = u.descargarArchivo(cat, nombreArchivo)
    return pathf

# def subirArchivo(cat, nombreArchivo):
#     if 
    
def procesarListaArchivos(catgeoria=None):
    ''' Verifica si es necesario generar una nueva cadena html para 
    mostrar la lista de archivos actualizada.
    '''
    pass
