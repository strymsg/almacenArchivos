# -*- coding: utf-8 -*-
'''
This file is part of Botadero
'''

from flask import Blueprint
from flask import render_template
from flask import request, redirect, send_from_directory, safe_join, send_file
from flask import url_for

#from botadero import app
from botadero import utils
from botadero import views

from werkzeug import secure_filename
from jinja2 import Environment, PackageLoader

import os

mod = Blueprint('archivos', __name__, url_prefix='/almacen')

@mod.route('/<path:filename>')
def donwload_file(filename):
    ''' Peticiones para descarga de archivos subidos
    TODO: Comprobar solo en categoria dada
    TODO: excepcion si el archivo no existe
    TODO: Enviar los archivos en pedazos para no sobre cargar la memoria
          * http://stackoverflow.com/questions/24318084/flask-make-response-with-large-files
          * http://stackoverflow.com/questions/5166129/how-do-i-stream-a-file-using-werkzeug/5166423#5166423
    '''
    # para no permitir descargar archivos no permitidos
    if '..' in filename or filename.startswith('/'):
        print "[DOWNLOAD] - Not allowed download detected: %s" %filename
        abort(404)

    utils.EstadisticaArchivos.IncrementarNumDescargas(os.path.join(app.config['UPLOAD_FOLDER'], \
                                                                   filename))
    

    pathf = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
    print "[DOWNLOAD] - abspath to file: %s" %pathf
    return send_file(pathf, as_attachment=True)

    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, \
                               as_attachment=True)
    BUG?
    # u'/home/strysg/Desarrollo/Webs/flask/botaderop/botadero/almacen/TheReturnOfTheAquabats.ogg'
    # ver issue #1169 y https://github.com/pallets/flask/pull/921
    '''

@mod.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    ''' Funcion para subir archivos
    TODO: Subir los archivos por pedazos.
    TODO: Evaluar la categoria para subir en el directorio correspondiente.
    TODO: agregar captcha? '''

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
            aux = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if utils.EstadisticaArchivos.AgregarArchivo(aux, sha1sum, file) != 0:
                # mostrar error en pantalla
                return views.mostrar_err_archivo_duplicado(sha1sum=sha1sum, nombre=filename)
                #return redirect('/estadisticas', code=302)

        return redirect("/", code=302)
        # http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    else:
        return "Aaah?"
