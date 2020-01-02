'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
# El objetivo de este archivo es albergar la logica compleja del botadero
import os

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

# def subirArchivo(cat, nombreArchivo):
#     if 

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

def marcarPaginaListaParaRenderizar(categoria):
    ''' Marca la pagina de la lista para renderizar de la categoria dada
    para que se vuelva a renderizar el template usando jinja2
    
    :param: True si se ha marcado correctamente, False en otro caso
    '''
    if categoria == 'Misc':
        categoria = globalParams.uploadDirectory
    # buscando el registro
    name = 'lista_archivos_' + categoria
    html_page = HtmlPage.query.filter_by(name=name).first()
    if htlm_page is not None:
        # modificando
        try:
            html_page.save(renderHtml=True)
            return True
        except Exception as E:
            print ('Excepcion modificando html_page %r', (name))
            return False
    return False
        
        
def procesarListaArchivos(catgeoria=None):
    ''' Verifica si es necesario generar una nueva cadena html para 
    mostrar la lista de archivos actualizada.
    '''
    pass
