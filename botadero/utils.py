'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
import os, sys, hashlib, re, random
from datetime import datetime as dt

from .shared import globalParams
from .database import get_db
from .database.models import Archivo

from flask import Flask

def registrarArchivo(self, nombreYRuta, hashCheck=False, hashAlgorithm=None, accelerateHash=False):
    ''' Dado un archivo en el sistema de archivos hace una serie de comprobaciones 
    y lo registra en la base de datos como un nuevo archivo.

    retorna el objeto creado o si existe el que esta en la BD.
    '''
    archivo = Archivo()

    # obtener la ruta completa
    
    # obtener informacion basica del archivo (del sistema de archivos)
    
    # comprobar si existe o no en la BD

    # si no existe obtener estadisticas e introducir en la BD
    return archivo

def hashArchivo(nombreYRuta, hashAlgorithm=None, accelerateHash=False):
    ''' Retorna el hexdigest del archivo usando los parametros dados
    '''
    if hashAlgorithm is None:
        hashAlgo = globalParams.digestAlgorithm
        if hashAlgo not in ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'):
            hashAlgo = 'sha1'

    h = None
    if hashAlgo == 'md5':
        h = hashlib.md5()
    elif hashAlgo == 'sha1':
        h = hashlib.sha1()
    elif hashAlgo == 'sha224':
        h = hashlib.sha224()
    elif hashAlgo == 'sha256':
        h = hashlib.sha256()
    elif hashAlgo == 'sha384':
        h = hashlib.sha384()
    elif hashAlgo == 'sha512':
        h = hashlib.sha512()

    with open(nombreYRuta, 'rb') as fil:
        if accelerateHash:
            fsize = os.path.getsize(nombreYRuta)
            # se divide el archivo en pedazos y se comprueba solo esos pedazos
            i = 0
            puntero = 0
            while puntero < fsize:
                # pedazos que crecen a razon de 1MiB
                cad = fil.read(i*1024*1024)
                h.update(cad)
                fil.seek(i*10*1024*1024, os.SEEK_CUR)
                puntero = fil.tell()
                i += 1
        else:
            # comprobando en pedazos de hasta 125 MiB
            pedazoTam = 125*1024*1024
            cad = fil.read(pedazoTam)
            h.update(cad)
            tAnt = -1
            tAct = fil.tell()
            while tAnt != tAct:
                cad = fil.read(pedazoTam)
                h.update(cad)
                tAnt = tAct
                tAct = fil.tell()
    return h.hexdigest()

def edadArchivo(nombreYRuta):
    ''' Retorna la edad o tiempo (en la unidad de tiempo usada globalmente)
    desde que el archivo ha sido creado '''
    return 0

def nombreArchivo(nombreYRuta):
    tupla = nombreYRuta.split(os.sep)
    return tupla[-1]

def extensionArchivo(nombreYRuta):
    if len(nombreYRuta.split('.')) > 1:
        return nombreYRuta.split('.')[-1]

def categoriaArchivo(self, nombreYRuta):
    tupla = nombreYRuta.split(os.sep)
    if len(tupla) > 2:
        return tupla[-2]
    return ''

def existeArchivo(nombreYRuta, comprobarCategoria=False, hashCheck=None):
    ''' Comprueba si el archivo dado esta registrado en la BD 
    usando los parametros dados.
    '''
    return False

def listaDeArchivosEnBd(categoria=None):
    ''' retorna la lista de archivos (registrados en la BD)
    :param categoria: si se proporciona, solo reotrna la lista de archivos
    que corresponde a esa categoria, si no se proporciona devuelve la 
    lista completa de todos los archivos.
    '''
    lista = []
    qLista = Archivo.query.all()
    for archivo in qLista:
        print (archivo)
    lista = qLista
    return lista

def listaDeArchivos(categoria=None, ignorar=[], orden='fecha_asc'):
    ''' retorna la lista de nombres de archivos (en la carpeta donde se almacenan los archivos) esten o no en la BD.

    :param categoria: si se proporciona solo busca en la carpeta correspondiente a la categoria dada.

    :param ignorar: Una lista con expresiones regulares para omitir nombres de archivos que coincidan.

    :param orden: de opciones multiples
    - fecha_asc: ordena por fecha de modificacion acendentemente (mas reciente primero)
    - fecha_des: ordena por fecha de modificacion decendentemetne.
    '''
    lista = []
    ruta = globalParams.uploadDirectory
    try:
        ow = os.walk(ruta)
        p,d,files = next(ow)
    except OSError:
        print ("[REG] - Error: Can't os.walk() on %s except OSError.")
    else:
        lista = [os.path.join(ruta, f) for f in files]
        reverse = False
        if orden == 'fecha_asc':
            reverse = True
        lista.sort(key=lambda x: os.path.getmtime(x), reverse=reverse)
    return lista

def borrarArchivo(nombreYRuta):
    ''' Elimina del sistema de archivos y el registro en la BD el archivo dado
    :return boolean: True o False si se elimina correctamente.
    '''
    return True

def comprobarTiempoArchivo(nombreYRuta):
    ''' comprueba si el archivo dado ha sobrepasado o no su tiempo permitido.
    '''
    return False

def comprobarPassword(nombreYRuta, password):
    ''' Consulta en la BD y comprueba si el archivo ha sido guardado usando el password dado.
    '''
    return True

def esquemaColoresRandom():
    '''
    devuelve un esquema de colores random de los definidos en static/
    '''
    esquemas = ('gris1', 'neutral','verde1','azul1','amarillo1', 'rojo1','cafe1')
    return esquemas[random.randint(0, len(esquemas) - 1)]
