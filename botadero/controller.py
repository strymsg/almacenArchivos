'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
from .shared import globalParams, gr
from . import utils as u
from botadero.database import get_db
from botadero.database.models import Archivo

def procesarListaArchivos(catgeoria=None):
    ''' Verifica si es necesario generar una nueva cadena html para 
    mostrar la lista de archivos actualizada.
    '''
    pass


