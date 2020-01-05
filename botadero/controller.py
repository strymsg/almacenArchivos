'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
# El objetivo de este archivo es albergar la logica de gestion de archivos y comportamiento general de la aplicacion
import os
from datetime import datetime as dt
from werkzeug.utils import secure_filename

from .shared import globalParams, gr
from . import utils as u
from .database.models import Archivo, HtmlPage

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

def subirArchivo(cat, file, hashedPassword=''):
    ''' Verifica el archivo siendo subido, lo guarda en el directorio de
    almacenamiento y lo registra en la BD. Tambien marca la categoria a la
    que pertenece el archivo para que se renderize el html de listado.

    :param cat: Categoria o subcarpeta donde se guarda el archivo
    :param file: objeto instancia de 'FileStorage' (werkzeug) del archivo

    :return: Si la subida es exitosa, retorna el registro en la base de 
    datos recien creado. Si no, retorna un diccionario de la forma:
    { tipoError: (entero), 
      mensaje: 'mensaje de error', 
      redirect: 'link redireccion en caso de ya existir un archivo'
    }

    NOTA: En caso de subir exitosamente, la funcion que lo llama deberia
    llamar a sincronizarArchivo() para actualizar los registros.
    '''
    print('subirArchivo(cat="%r", file="%r", hashedPassword="%r"' % (cat, file, hashedPassword))
    filename = secure_filename(file.filename)
    categoria = ''
    if cat != 'Misc':
        categoria = cat
    # comprobando existencia
    filepath = os.path.join(globalParams.uploadDirectory, categoria, filename)
    try:
        f = open(filepath, 'r')
        f.close()
        print('Archivo siendo subido ya existe:', filepath)
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
            print ('Ya existe un archivo con el mismo digestCheck ', digestCheck, 'encontrado', str(regDb))
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

    # TODO: comprobar espacio de almacenamiento disponible
    # ...
    
    # guardando en el sistema de archivos
    try:
        file.save(os.path.join(globalParams.uploadDirectory, categoria, filename))
        print('✓ Archivo guardado en sistema de archivos: %r' % os.path.join(globalParams.uploadDirectory, categoria, filename))
    except Exception as E:
        print('✕ Excepcion al guardar archivo %r en el sistema de archivos:\n%r' % (filename, str(E)))
        return {
            'tipoError': 4,
            'mensaje': 'Error interno al guardar el archivo ' + filename,
            'redirect': categoria
        }
    # creando registro en la BD
    arch = Archivo.create(name=filename,
                          path=filepath, size=fsize,
                          extension=u.extensionArchivo(filename),
                          digestCheck=digestCheck,
                          digestAlgorithm=globalParams.digestAlgorithm,
                          uploadedAtTime=uploadedAtTime,
                          remainingTime=remainingTime,
                          hashedPassword=hashedPassword)
    print('✓ Archivo registrado en BD', arch)
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
        print ('archivo:', archivo.name, '  edad:', str(edad),  'borrado max', str(tiempoBorrado))
        if (tiempoBorrado < edad):
            r = u.borrarArchivo(archivo.path)
            print (' xx Borrando archivo', archivo.name, ' = ', r)
            
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
            print('modificado::::::::', html_page.name, str(html_page.renderHtml))
            return True
        except Exception as E:
            print ('Excepcion modificando html_page %r', (name))
            return False
    return False

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
    print ('** Sincronizando archivos **')
    print ('\nParametros', str(globalParams))
    listaEnBd = u.listaDeArchivosEnBd()
    archivosEnBd = []
    for reg in listaEnBd:
        archivosEnBd.append(reg.path)
    
    archivos = []

    listaLsArchivos = []
    registrados = []
    borrados = []
    actualizados = []

    # obteniendo lista de archivos en el sistema de archivos
    print('#' + 'Misc')
    lista = u.listaDeArchivos()
    for archivo in lista:
        if u.nombreArchivo(archivo) not in ignorar:
            # estandarizando nombre
            print(os.path.join(os.path.curdir + os.path.sep, archivo))
            archivos.append(os.path.join(os.path.curdir + os.path.sep, archivo))
    
    for cat in u.categorias():
        print('#' + cat)
        lista = u.listaDeArchivos(categoria=cat)
        for archivo in lista:
            if u.nombreArchivo(archivo) not in ignorar:
                # estandarizando nombre
                print(os.path.join(os.path.curdir + os.path.sep, archivo))
                archivos.append(os.path.join(os.path.curdir + os.path.sep, archivo))

    # actualizando BD
    for archivo in archivos:
        if archivo in ignorar:
            continue
        if archivo not in archivosEnBd:
            print ('(+)', str(archivo), u.categoriaArchivo(archivo))
            arch = u.registrarArchivo(archivo)
            marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivo))
            registrados.append(arch)
        else:
            if u.archivoDebeBorrarsePorTiempo(archivo):
                print ('(-)', str(archivo), u.categoriaArchivo(archivo))
                r = u.borrarArchivo(archivo) # del sistema de archivos y BD
                borrados.append(archivo)
                print (' ✗ Registro de archivo borrado', archivo, ' = ', r)
                marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivo))
            else:
                if u.actualizarTiempoRestanteArchivo(archivo):
                    print ('(+-)', str(archivo), u.categoriaArchivo(archivo))
                    actualizados.append(archivo)
                    marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(archivo))
    for reg in archivosEnBd:
        # caso de que un archivo se borro del sistema de archivos
        if reg not in archivos:
            print('(bd -)', str(reg), u.categoriaArchivo(reg))
            r = u.borrarRegistroArchivoEnBd(u.nombreArchivo(reg))
            borrados.append(reg)
            marcarPaginaListaParaRenderizar(categoria=u.categoriaArchivo(reg))

    print ('\nsincronización completa')
    return registrados, borrados, actualizados

