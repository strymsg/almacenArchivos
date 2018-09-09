'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
import os, sys, hashlib, re, random
from datetime import datetime as dt
from sqlalchemy import desc

from . import shared
from .database import get_db
from .database.models import Archivo

from flask import Flask

def registrarArchivo(nombreYRuta, digestCheck=None, digestAlgorithm=None, accelerateHash=False, hashedPassword=''):
    ''' Dado un archivo en el sistema de archivos hace una serie de comprobaciones 
    y lo registra en la base de datos como un nuevo archivo.

    retorna el objeto creado o si existe el que esta en la BD.
    '''
    # comprobar si existe o no en la BD
    archivo = existeArchivo(nombreYRuta)
    if archivo is not None:
        return archivo
        
    # si no existe obtener estadisticas e introducir en la BD
    # obtener la ruta completa
    rutaCompleta = os.path.realpath(nombreYRuta)
    rutaRelativa = addRelativeFileName(nombreYRuta)
    path = rutaRelativa
    # obtener informacion basica del archivo (del sistema de archivos)
    size = os.path.getsize(nombreYRuta)
    extension = extensionArchivo(nombreYRuta)
    # obtener hashcheck del archivo
    _digestCheck = ''
    _digestAlgorithm = ''
    if digestAlgorithm is None:
        _digestAlgorithm = shared.globalParams.digestAlgorithm
    if digestCheck is None:
        if shared.globalParams.digestCheck:
            _accelerateHash = accelerateHash
            if _accelerateHash is None:
                _accelerateHash = shared.globalParams.accelerateHash
            _digestCheck = hashArchivo(rutaCompleta, hashAlgorithm=_digestAlgorithm, accelerateHash=_accelerateHash)
    elif digestCheck == True:
        _accelerateHash = accelerateHash
        if _accelerateHash is None:
            _accelerateHash = shared.globalParams.accelerateHash
        _digestCheck = hashArchivo(rutaCompleta, hashAlgorithm=_digestAlgorithm, accelerateHash=_accelerateHash)
    # determinar tiempo de eliminacion
    remainingTime = tiempoBorradoArchivo(size)
    uploadedAtTime = dt.now()
    # creando registro en la BD
    arch = Archivo.create(name=nombreArchivo(nombreYRuta),
                          path=path, size=size,
                          extension=extensionArchivo(nombreYRuta),
                          digestCheck=_digestCheck,
                          digestAlgorithm=_digestAlgorithm,
                          uploadedAtTime=uploadedAtTime,
                          remainingTime=remainingTime,
                          hashedPassword=hashedPassword)
    return arch

def hashArchivo(nombreYRuta, hashAlgorithm=None, accelerateHash=False):
    ''' Retorna el hexdigest del archivo usando los parametros dados
    '''
    hashAlgo = 'sha1'
    if hashAlgorithm is None:
        hashAlgo = shared.globalParams.digestAlgorithm
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

def edadArchivo(nombreYRuta, archivo=None):
    ''' Retorna la edad o tiempo (en la unidad de tiempo usada globalmente)
    desde que el archivo ha sido creado '''
    if archivo is None:
        archivo = existeArchivo(nombreYRuta)
    uploadedAtTime = dt.strptime(archivo.uploadedAtTime, '%Y-%m-%d %H:%M:%S.%f')
    if archivo is None:
        return -1
    if shared.globalParams.timeUnit == 'day':
        return (dt.now() - uploadedAtTime).days
    elif shared.globalParams.timeUnit == 'minute':
        return (dt.now() - uploadedAtTime).min
    elif shared.globalParams.timeUnit == 'second':
        return (dt.now() - uploadedAtTime).seconds
    return 0

def nombreArchivo(nombreYRuta):
    tupla = nombreYRuta.split(os.sep)
    return tupla[-1]

def extensionArchivo(nombreYRuta):
    if len(nombreYRuta.split('.')) > 1:
        return nombreYRuta.split('.')[-1]

def categoriaArchivo(nombreYRuta):
    tupla = nombreYRuta.split(os.sep)
    if len(tupla) > 2:
        return tupla[-2]
    return ''

def existeArchivo(nombreYRuta, comprobarCategoria=False, hashCheck=None):
    ''' Comprueba si el archivo dado esta registrado en la BD 
    usando los parametros dados. Retorna el Objeto Archivo o None
    '''
    nombre = nombreArchivo(nombreYRuta)
    #path = categoriaArchivo(nombreYRuta)
    path = addRelativeFileName(nombreYRuta)
    print('>>>>>>>>>>', path)
    return Archivo.query.filter_by(name=nombre, path=path).first()

def listaDeArchivosEnBd(categoria=None, ignorar=[]):
    ''' retorna la lista de archivos (registrados en la BD)
    :param categoria: si se proporciona, solo reotrna la lista de archivos
    que corresponde a esa categoria, si no se proporciona devuelve la 
    lista completa de todos los archivos.
    '''
    lista = []
    qLista = Archivo.query.order_by(desc(Archivo.uploadedAtTime)).all()
    for archivo in qLista:
        if archivo.name not in ignorar:
            if categoria is not None:
                if  categoriaArchivo(archivo.path) == categoria:
                    lista.append(archivo)
            else:
                lista.append(archivo)
    return lista

def listaDeArchivos(categoria=None, orden='fecha_asc'):
    ''' retorna la lista de nombres de archivos (en la carpeta donde se almacenan los archivos) esten o no en la BD.

    :param categoria: si se proporciona solo busca en la carpeta correspondiente a la categoria dada.

    :param orden: de opciones multiples
    - fecha_asc: ordena por fecha de modificacion acendentemente (mas reciente primero)
    - fecha_des: ordena por fecha de modificacion decendentemetne.
    '''
    lista = []
    ruta = shared.globalParams.uploadDirectory
    if categoria is not None:
        ruta = os.path.join(shared.globalParams.uploadDirectory, categoria)
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

def borrarArchivo(nombreYRuta, archivo=None):
    ''' Elimina del sistema de archivos y el registro en la BD el archivo dado
    :return boolean: True o False si se elimina correctamente.
    '''
    rutaCompleta = os.path.realpath(nombreYRuta) 
    try:
        os.remove(rutaCompleta)
    except Exception as E:
        print ('No se pudo borrar el archivo', rutaCompleta, 'E:', str(E))
        return False
    return Archivo.query.filter_by(path=nombreYRuta).first().delete() is None


def tiempoBorradoArchivo(size):
    ''' retorna el tiempo en que el archivo debe ser borrado 
    '''
    timeToDel = 0
    for lim in shared.globalParams.sizeLimitsAndTimeToDelete:
        if int(size) <= int(lim[0]):
            return int(lim[1])
        else:
            timeToDel = int(lim[1])
    return timeToDel

def comprobarTiempoArchivo(nombreYRuta, archivo=None):
    ''' comprueba si el archivo dado ha sobrepasado o no su tiempo permitido.
    '''
    if archivo is None:
        archivo = Archivo.query.filter_by(path=nombreYRuta).first()
    
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

def addRelativeFileName(filename):
    print ('filename', filename)
    if not filename.startswith(os.path.sep) or not filename.startswith('.'):
        print ('ret:::', os.path.join((os.path.curdir + os.path.sep), filename))
        return os.path.join((os.path.curdir + os.path.sep), filename)
    print ('ret:', filename)
    return filename

def categorias():
    ''' Devuelve la lista de categorias (carpetas) dentro el directorio
    de subidas
    '''
    ow = os.walk(os.path.realpath(shared.globalParams.uploadDirectory))
    return next(ow)[1] # directorios en el primer nivel

def descargarArchivo(cat, nombreArchivo):
    ''' Devuelve la ruta para descargar (enviar el archivo al cliente) e
    incrementa su contador de descargas'''
    # print(cat, '"',nombreArchivo,'"')
    pathf = '' # para ruta absoluta
    pathr = '' # para ruta relativa
    # rutas
    if cat != 'Misc':
        pathr = addRelativeFileName(
            os.path.join(shared.globalParams.uploadDirectory, cat,
                         nombreArchivo))
        pathf = os.path.join(
            os.path.abspath(shared.globalParams.uploadDirectory), cat,
            nombreArchivo)
    else:
        pathr = addRelativeFileName(
            os.path.join(shared.globalParams.uploadDirectory, nombreArchivo))
        pathf = os.path.join(
            os.path.abspath(shared.globalParams.uploadDirectory),
            nombreArchivo)

    # consultando en BD
    archivo = Archivo.query.filter_by(path=pathr).first()
    if archivo is None:
        return None
    archivo.save(downloads=archivo.downloads + 1)
    return pathf
    
def sincronizarArchivos(ignorar=[]):
    ''' Lista los archivos en el directorio de subidas y los introduce en
    la base de datos si estos no estan registrados.

    Retorna dos listas, una los archivos en el sistema de archivos y otra los registrados en BD

    :param ignorar: Una lista con nombres de archivos a ignorar
    '''
    print ('** Sincronizando archivos **')
    print ('\nParametros', str(shared.globalParams));
    archivosEnBD = []
    listaLsArchivos = []
    for cat in categorias():
        print ('#' + cat)
        lista = listaDeArchivos(categoria=cat)
        for archivo in lista:
            print ('  ', archivo)
            if nombreArchivo(archivo) not in ignorar:
                arch = registrarArchivo(archivo)
                archivosEnBD.append(arch.path)
                listaLsArchivos.append(archivo)
    lista = listaDeArchivos()
    for archivo in lista:
        print (' ', archivo)
        if nombreArchivo(archivo) not in ignorar:
            arch = registrarArchivo(archivo)
            archivosEnBD.append(arch.path)
            listaLsArchivos.append(archivo)
    print ('\nsincronizacion completa')
    return listaLsArchivos, archivosEnBD

def listaArchivosParaRenderizar(categoria=None, ignorar=[]):
    ''' Devuelve un diccionario con la lista de archivos registrados 
    en la base de datos en un formato conveniete para ser mostrado en
    el sitio frontal web.

    :param categoria: Si se proporciona solo retorna la lista de
    archivos de esa categoria.

    Ej:
    [ {'name': 'archi1.jpeg', 'size': 4991, date: '2018-06-14 19:49:17.427922', 'restante': 2},
      {'name': 'arc.jpeg', 'size': 199, date: '2018-08-14 19:49:17.427922', 'restante': 2},
      {'name': '9g.mp3', 'size': 83981, date: '2018-08-14 19:49:19.427922', 'restante': 9}
    ]
    '''
    lista = []
    if categoria is not None:
        if categoria == 'Misc':
            # caso especial
            lista = listaDeArchivosEnBd(categoria='almacen', ignorar=ignorar)
        else:
            lista = listaDeArchivosEnBd(categoria=categoria, ignorar=ignorar)
    else:
        lista = listaDeArchivosEnBd(ignorar=ignorar)
    archivos = []
    for archivo in lista:
        obj = {
            'name':archivo.name,
            'size':archivo.size,
            'date':archivo.uploadedAtTime,
            'restante':archivo.remainingTime
        }
        archivos.append(obj)
    return archivos
