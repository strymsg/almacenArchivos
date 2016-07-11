# -*- coding: utf-8 -*-
'''
This file is part of Botadero
'''

from flask import Blueprint
from flask import render_template
from flask import request, redirect, send_from_directory, safe_join, send_file, abort
from flask import url_for

#from botadero import app
from botadero import utils
from botadero import views

from werkzeug import secure_filename
from jinja2 import Environment, PackageLoader

import os

mod = Blueprint('archivos', __name__, url_prefix='/almacen')

UploadFolder = utils.EstadisticaArchivos.Parametros.UploadFolder

@mod.route('/<path:filename>')
def donwload_file(filename):
    ''' Peticiones para descarga de archivos subidos
    TODO: excepcion si el archivo no existe
    TODO: Enviar los archivos en pedazos para no sobre cargar la memoria
          * http://stackoverflow.com/questions/24318084/flask-make-response-with-large-files
          * http://stackoverflow.com/questions/5166129/how-do-i-stream-a-file-using-werkzeug/5166423#5166423
    '''
    pathf = os.path.join(os.path.abspath(UploadFolder), filename)

    # para no permitir descargar archivos no permitidos
    if '..' in filename or filename.startswith('/'): #or pathf.index(os.sep) >= 0:
        print "[DOWNLOAD] - Not allowed download detected: %s" %filename
        abort(404)
    
    utils.EstadisticaArchivos.IncrementarNumDescargas(os.path.join(UploadFolder,\
                                                                   filename))


    print "[DOWNLOAD] - abspath to file: %s" %pathf
    return send_file(pathf, as_attachment=True)
    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, \
                               as_attachment=True)
    BUG?
    # u'/home/strysg/Desarrollo/Webs/flask/botaderop/botadero/almacen/TheReturnOfTheAquabats.ogg'
    # ver issue #1169 y https://github.com/pallets/flask/pull/921
    '''

# NOTA.- No es necesario agregar /almacen/upload_file en la ruta por que
# el constructir del Blueprint contiene : url_prefix='/almacen'
@mod.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    ''' Funcion para subir archivos en categoria "" o Misc.
    TODO: Subir los archivos por pedazos.
    TODO: agregar captcha? '''

    utils.EstadisticaArchivos.Actualizar()
    if request.method == 'POST':
        file = request.files['file'] #devuelve tipo FileStorage
        filename = ''
        if file:
            filename = secure_filename(file.filename)
            # TODO: Ver la forma de hacer el checksum a medida
            # los datos van llegando con haslib.update() para no
            # copiar el archivo (evitar duplicacion)
            da = utils.DatosDeArchivo()
            sha1sum = da.arch_sha1sum(file)
            print "[UPLOAD] - Request to upload File %s" %filename\
                ,"            checksum %s" % sha1sum
            
            # restaura el puntero
            file.seek(0)
            aux = os.path.join(UploadFolder, filename)
            if utils.EstadisticaArchivos.AgregarArchivo(aux, sha1sum, file) != 0:
                # mostrar error en pantalla
                return views.mostrar_err_archivo_duplicado(sha1sum=sha1sum, nombre=filename)
                #return redirect('/estadisticas', code=302)

        return redirect("/", code=302)
        # http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    else:
        return "Aaah?"

@mod.route('/<cat>/upload_file', methods=['POST'])
def upload_file_cat(cat):
    ''' Funcion para subir archivos segun categoria
    TODO: Subir los archivos por pedazos.
    TODO: agregar captcha? '''

    utils.EstadisticaArchivos.Actualizar()
    categorias = utils.categorias()
    categoria_actual = ''
    categorias = [""] + categorias # dummy
    if cat in categorias:
        categoria_actual = cat
    else:
        return "La categoria %s no se ha encontrado." %cat # TODO: redirigir a pagina error en categoria
    
    if request.method == 'POST':
        file = request.files['file'] #devuelve tipo FileStorage
        filename = ''
        if file:
            filename = secure_filename(file.filename)
            # TODO: Ver la forma de hacer el checksum a medida
            # los datos van llegando con haslib.update() para no
            # copiar el archivo (evitar duplicacion)
            da = utils.DatosDeArchivo()
            sha1sum = da.arch_sha1sum(file)
            print "[UPLOAD] - Request to upload File %s" %filename ,\
                " to category #%s" %cat \
                ,"            checksum %s" % sha1sum
            
            # restaura el puntero
            file.seek(0)
            aux = os.path.join(UploadFolder, cat, filename)
            if utils.EstadisticaArchivos.AgregarArchivo(aux, sha1sum, file) != 0:
                # mostrar error en pantalla
                return views.mostrar_err_archivo_duplicado(sha1sum=sha1sum, nombre=filename)
                #return redirect('/estadisticas', code=302)

        return redirect("/"+cat, code=302)
        # http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    else:
        return "Aaah?"
    

    
