'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
# El objetivo de este archivo es albergar la logica de gestion de archivos y comportamiento general de la aplicacion
import os
from datetime import datetime as dt
from werkzeug.utils import secure_filename
from flask import g

from .shared import globalParams, gr
from . import utils as u
from .database.models import Archivo, HtmlPage

log = g.log

def descargaPermitida(cat, nombreArchivo):
    if '..' in nombreArchivo or nombreArchivo.startswith(os.path.sep):
        return False
    if cat not in u.categorias() and cat != 'Misc':
        return False
    return True

def tienePassword(nombreArchivo):
    regDb = Archivo.query.filter_by(name=nombreArchivo).first()
    if regDb is not None:
        return len(regDb.hashedPassword) > 0
    else:
        return False

def descargarArchivo(cat, nombreArchivo, password=''):
    ''' Ayuda a descargar un archivo, retornando la ruta del archivo
    - cat (string): Categoria del archivo.
    - nombreArchivo (string):  Nombre del archivo.
    - password (string): (opcional) Si el archivo esta protegido requiere
      un password
    :return (string) pathfile o en caso de error un diccionario de la forma
    {
        'tipoError': 2,
        'mensaje': 'Contraseña incorrecta'
    }
    '''
    # obteniendo ruta del archivo
    pathf = u.descargarArchivo(cat, nombreArchivo)
    if pathf is None:
        return {
            'tipoError': 1,
            'mensaje': 'Error buscando el archivo'
        }
    # comprobando password si es necesario
    if password != '':
        if u.comprobarPassword(pathf, password) is False:
            return {
                'tipoError': 2,
                'mensaje': 'Contraseña incorrecta'
            }
    
    # marcando para que se actualice el renderizado de la pagina
    marcarPaginaListaParaRenderizar(categoria=cat)
    return pathf

def subirArchivo(cat, file, password=''):
    ''' Verifica el archivo siendo subido, lo guarda en el directorio de
    almacenamiento y lo registra en la BD. Tambien marca la categoria a la
    que pertenece el archivo para que se renderize el html de listado.

    :param cat: Categoria o subcarpeta donde se guarda el archivo.
    :param file: objeto instancia de 'FileStorage' (werkzeug) del archivo.
    :param password: Cadena con el password si es '' no se usa.

    :return: Si la subida es exitosa, retorna el registro en la base de 
    datos recien creado. Si no, retorna un diccionario de la forma:
    { tipoError: (entero), 
      mensaje: 'mensaje de error', 
      redirect: 'link redireccion en caso de ya existir un archivo'
    }

    NOTA: En caso de subir exitosamente, la funcion que lo llama deberia
    llamar a sincronizarArchivo() para actualizar los registros.
    '''
    log.debug('^ subirArchivo(cat="{0}", file="{1}"'.format(cat, file))
    filename = secure_filename(file.filename)
    categoria = ''
    if cat != 'Misc':
        categoria = cat
    # comprobando existencia
    filepath = os.path.join(globalParams.uploadDirectory, categoria, filename)
    filepath = u.addRelativeFileName(filepath)

    # nombre del archivo
    if len(filename) < 1:
        log.debug('El archivo "{0}" se ha traducido en el nombre "{1}" que tiene un nombre válido'
                  .format(file.filename, filename))
        return {
            'tipoError': 5,
            'mensaje': 'El archivo no tiene un nombre válido',
            'redirect': categoria
        }

    try:
        f = open(filepath, 'r')
        f.close()
        log.debug('Archivo siendo subido ya existe: {0}'.format(filepath))
        return {
            'tipoError': 1,
            'mensaje': 'El archivo "' + filename + '" ya existen en ' + filepath,
            'redirect': categoria
        }
    except IOError as E:
        pass

    # comprobando hash
    digestCheck = ''
    if globalParams.digestCheck:
        digestCheck = u.hashFileStorage(file,
                                        accelerateHash=globalParams.digestAccelerated)
        regDb = Archivo.query.filter_by(digestCheck=digestCheck).first()
        if regDb is not None:
            # existe un registro con el mismo digestCheck
            file.close()
            cat = u.categoriaArchivo(regDb.path)
            if cat == globalParams.uploadDirectory:
                cat = ''
            cat += '/'
            log.debug('Ya existe un archivo con el mismo digestCheck {0} encontrado {1}'
                      .format(digestCheck, str(regDb)))
            return {
                'tipoError': 2,
                'mensaje': 'Ya existe un archivo con el mismo digestCheck ' + digestCheck + ' con nombre ' + regDb.name,
                'redirect': categoria + regDb.name
            }

    # procediendo a registrar el archivo en BD
    file.seek(0, os.SEEK_END)
    fsize = file.tell()
    file.seek(0)

    remainingTime = u.tiempoBorradoArchivo(fsize)
    uploadedAtTime = dt.now()

    # comprobando espacio de almacenamiento disponible
    if gr['storageUsed'] == 0:
        u.actualizarEstadisticasGenerales()
    if gr['storageUsed'] + fsize > gr['storageTotal']:
        log.warning('No se cuenta con espacio de almacenamiento suficiente, requiere {0} se cuenta {1}'
                    .format(str(fsize), str(gr['storageTotal'] - gr['storageUsed'])))
        return {
            'tipoError': 3,
            'mensaje': 'No se cuenta con espacio suficiente',
            'redirect': categoria
        }
    
    # guardando en el sistema de archivos
    try:
        file.save(os.path.join(globalParams.uploadDirectory, categoria, filename))
        log.info('✓ Archivo guardado en sistema de archivos: {0}'
                 .format(os.path.join(globalParams.uploadDirectory, categoria, filename)))
    except Exception as E:
        log.error('✕ Excepcion al guardar archivo %r en el sistema de archivos: {0}\n{1}'
                  .format((filename, str(E))))
        return {
            'tipoError': 4,
            'mensaje': 'Error interno al guardar el archivo ' + filename,
            'redirect': categoria
        }

    if len(Archivo.query.filter_by(name=filename).all()) > 1:
        log.warning('Ya existe un archivo en la BD con nombre: {0} '.format(filename))
        return {
            'tipoError': 1,
            'mensaje': 'Ya existe (BD) un archivo con nombre ' + filename,
            'redirect': categoria
        }        

    hashedPassword = ''
    if password != '':
        hashedPassword = u.hashPassword(password)

    # creando registro en la BD
    arch = Archivo.create(name=filename,
                          path=filepath, size=fsize,
                          extension=u.extensionArchivo(filename),
                          digestCheck=digestCheck,
                          digestAlgorithm=globalParams.digestAlgorithm,
                          uploadedAtTime=uploadedAtTime,
                          remainingTime=remainingTime,
                          hashedPassword=hashedPassword)
    # sincronizarArchivos(['.gitkeep', '.gitkeep~', '#.gitkeep', '#.gitkeep#'])
    log.info('✓ Archivo registrado en BD {0} {1}'.format(str(arch), str(len(arch.hashedPassword))))
    return arch
    
    
# definir una funcion para comprobar la lista de archivos y su tiempo de 
# borrado
def comprobarTiempoBorradoListaArchivos(categoria, hdd=False):
    ''' Verifica si es necesario borrar archivos en los archivos dados en
    la carpeta (categoria) guradada en el almacen
    :param categoria: La carpeta (categoria) dentro el almacen donde se hace
    la busqueda.
    :param hdd: Hace que la busqueda se haga en el almacenamiento fisico (HDD tipicamente).
    :return borrados: Lista de archivos que se han borrado (directorios)
    '''
    # ajuste
    if categoria == 'Misc':
        categoria = globalParams.uploadDirectory
    lista = None
    if hdd:
        lista = u.listaDeArchivos(categoria)
    else:
        lista = u.listaDeArchivosEnBd(categoria)
    # print ('LISTA de archivos:::::::::::', str(lista))
    borrados = []
    for archivo in lista:
        tiempoBorrado = u.tiempoBorradoArchivo(archivo.size)
        edad = u.edadArchivo(archivo.path, archivo)
        log.info('archivo: {0}    edad: {1}  borrado max: {2}'
                 .format(archivo.name, str(edad), str(tiempoBorrado)))
        if (tiempoBorrado < edad):
            r = u.borrarArchivo(archivo.path)
            log.warning(' xx Borrando archivo {0} = {1}'.format(archivo.name,r))
            
            borrados.append(archivo.path)
    return borrados

def marcarPaginaListaParaRenderizar(categoria='Misc'):
    ''' Marca la pagina de la lista para renderizar de la categoria dada
    para que se vuelva a renderizar el template usando jinja2
    
    :param: True si se ha marcado correctamente, False en otro caso
    '''
    if categoria == globalParams.uploadDirectory or categoria == '':
        categoria = 'Misc' # ajuste por conveniencia
    # buscando el registro
    name = 'lista_archivos_' + categoria
    html_page = HtmlPage.query.filter_by(name=name).first()

    if html_page is not None:
        # modificando
        try:
            html_page.save(renderHtml=True)
            log.debug('marcado para generar html: {0} {1}'
                      .format(html_page.name, str(html_page.renderHtml)))
            return True
        except Exception as E:
            log.error('Excepcion modificando html_page {0}'.format(name))
            return False
    return False

def marcarTodasLasPaginasParaRenderizar():
    ''' Usa la funcion marcarPaginaListaParaRenderizar para marcar
    todas las paginas y que se vuelva a renderizar el template usando jinja2
    '''
    for cat in u.categorias():
        marcarPaginaListaParaRenderizar(categoria=cat)
    marcarPaginaListaParaRenderizar() # para categoria Misc

def sincronizarArchivos(ignorar=[]):
    ''' Funcion encargada sincronizar y actualizar la BD segun los archivos
    que se encuentran en el directorio de subidas en el sistema de archivos.

    Lista los archivos en el directorio de subidas y los introduce en
    la base de datos si estos no estan registrados. Tambien borra los 
    registros de archivos que se encuentran en la BD pero no en el sistema
    de archivos. Cuando detecta un cambio marca la pagina web necesaria para
    que se renderize.

    :param ignorar: Una lista con nombres de archivos a ignorar

    :return ([registrados],[borrados],[actualizados]): Retorna tres listas, segun registra nuevos archivos en BD, los borra o actualiza su tiempo restante.
    '''
    log.debug('** Sincronizando archivos **')
    log.debug('\nParametros\n {0}'.format(str(globalParams)))
    listaEnBd = u.listaDeArchivosEnBd()
    archivosEnBd = []
    for reg in listaEnBd:
        archivosEnBd.append(reg.path)
        # print('i ', reg.path)
    
    archivos = []

    listaLsArchivos = []
    registrados = []
    borrados = []
    actualizados = []

    # obteniendo lista de archivos en el sistema de archivos
    log.debug('# Misc')
    lista = u.listaDeArchivos()
    for archivo in lista:
        if u.nombreArchivo(archivo) not in ignorar:
            # estandarizando nombre
            log.debug(os.path.join(os.path.curdir + os.path.sep, archivo))
            archivos.append(os.path.join(os.path.curdir + os.path.sep, archivo))
    
    for cat in u.categorias():
        log.debug('# {0}'.format(cat))
        lista = u.listaDeArchivos(categoria=cat)
        for archivo in lista:
            if u.nombreArchivo(archivo) not in ignorar:
                # estandarizando nombre
                log.debug(os.path.join(os.path.curdir + os.path.sep, archivo))
                archivos.append(os.path.join(os.path.curdir + os.path.sep, archivo))

    # actualizando BD
    for archivo in archivos:
        # print('o ', archivo, archivo not in archivosEnBd)
        if archivo in ignorar:
            continue
        if archivo not in archivosEnBd:
            log.debug ('(+) {0} {1}'.format(str(archivo), u.categoriaArchivo(archivo)))
            arch = u.registrarArchivo(archivo)
            marcarTodasLasPaginasParaRenderizar()
            #marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivo))
            registrados.append(arch)
        else:
            if u.archivoDebeBorrarsePorTiempo(archivo):
                log.debug('(-) {0} {1}'.format(str(archivo), u.categoriaArchivo(archivo)))
                r = u.borrarArchivo(archivo) # del sistema de archivos y BD
                borrados.append(archivo)
                log.debug(' ✗ Registro de archivo borrado {0} = {1}'
                          .format(archivo, r))
                marcarTodasLasPaginasParaRenderizar()
                # marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivo))
            else:
                if u.actualizarTiempoRestanteArchivo(archivo):
                    log.debug('(+-) {0} {1}'.format(str(archivo), u.categoriaArchivo(archivo)))
                    actualizados.append(archivo)
                    marcarTodasLasPaginasParaRenderizar()
                    # marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivo))
    for reg in archivosEnBd:
        # caso de que un archivo se borro del sistema de archivos
        if reg not in archivos:
            log.debug('(bd -) {0} {1}'.format(str(reg), u.categoriaArchivo(reg)))
            r = u.borrarRegistroArchivoEnBd(u.nombreArchivo(reg))
            borrados.append(reg)
            marcarTodasLasPaginasParaRenderizar()
            # marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(reg))

    log.debug('\nsincronización completa')
    return registrados, borrados, actualizados

