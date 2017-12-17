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
from botadero import DatosDeArchivo

from werkzeug import secure_filename
from jinja2 import Environment, PackageLoader

import os
import json
import glob

mod = Blueprint('archivos', __name__, url_prefix='/almacen')

UploadFolder = utils.Ea.Parametros.UploadFolder
HashAlgorithm = utils.Ea.Parametros.HashAlgorithm
AccelerateHash = utils.Ea.Parametros.AccelerateHash

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
    
    utils.Ea.IncrementarNumDescargas(os.path.join(UploadFolder,\
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

    utils.Ea.Actualizar()
    if request.method == 'POST':
        print ("[UPLOAD] - Request to Upload file at: /")
        file = request.files['file'] #devuelve tipo FileStorage
        filename = ''
        if file:
            filename = secure_filename(file.filename)
            # TODO: Ver la forma de hacer el checksum a medida
            # los datos van llegando con haslib.update() para no
            # copiar el archivo (evitar duplicacion)
            #da = utils.DatosDeArchivo()
            da = DatosDeArchivo.DatosDeArchivo()
            print ("[UPLOAD] - Perparing to Apply: "+HashAlgorithm)
            hash_chk = da.arch_hash(file, hash_algorithm=HashAlgorithm, \
                                    accelerate=AccelerateHash)
            print "[UPLOAD] - Upload File: %s" \
                %filename\
                ,"            hash_check %s" % hash_chk
            
            name = os.path.join(UploadFolder, filename)
            if utils.Ea.AgregarArchivo(name, hash_chk, file) != 0:
                # mostrar error en pantalla
                return views.mostrar_err_archivo_duplicado(hash_check=hash_chk, nombre=filename)
            
        return redirect("/", code=302)
        # http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    else:
        return "Aaah?"

@mod.route('/<cat>/upload_file', methods=['POST'])
def upload_file_cat(cat):
    ''' Funcion para subir archivos segun categoria
    TODO: Subir los archivos por pedazos.
    TODO: agregar captcha? '''

    utils.Ea.Actualizar()
    categorias = utils.categorias()
    categoria_actual = ''
    categorias = [""] + categorias # dummy
    if cat in categorias:
        categoria_actual = cat
    else:
        return "La categoria %s no se ha encontrado." %cat # TODO: redirigir a pagina error en categoria
    
    if request.method == 'POST':
        file = request.files['file'] #devuelve tipo FileStorage
        print ("[UPLOAD] - Request to Upload file at: "+cat+"/")
        filename = ''
        if file:
            filename = secure_filename(file.filename)
            # TODO: Ver la forma de hacer el checksum a medida
            # los datos van llegando con haslib.update() para no
            # copiar el archivo (evitar duplicacion)
            da = utils.DatosDeArchivo()
            print ("[UPLOAD] - Perparing to Apply: "+HashAlgorithm)
            hash_chk = da.arch_hash(file, hash_algorithm=HashAlgorithm,\
                                    accelerate=AccelerateHash)
            print "[UPLOAD] - Request to upload File %s" %filename ,\
                " to category #%s" %cat \
                ,"            hash check %s" % hash_chk
            
            # restaura el puntero
            #file.seek(0)
            aux = os.path.join(UploadFolder, cat, filename)
            if utils.Ea.AgregarArchivo(aux, hash_chk, file) != 0:
                # mostrar error en pantalla
                return views.mostrar_err_archivo_duplicado(hash_check=hash_chk, nombre=filename)

        return redirect("/"+cat, code=302)
        # http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    else:
        return "Aaah?"

@mod.route("/upload_file_a", methods=['POST'])
def upload_file_ajax():
    ''' Funcion para subir archivos mediante peticiones ajax
    '''
    form = request.form
    print ("[UPLOAD-ajax]")
    
    # Is the upload using Ajax, or a direct POST by the form?
    if form.get("__ajax", None) != "true":
        return ajax_response("error", "Invlalid request")
        
    if request.method == 'POST':
        for key, value in form.items():
            print (key, "=>", value)

    agregados = []
    no_agregados = []
            
    utils.Ea.Actualizar()
    # Procesando cada archivo enviado en la peticion.
    for upload in request.files.getlist("file"):
        filename = secure_filename(upload.filename)
        print (" Incoming file:", filename)
        
        da = DatosDeArchivo.DatosDeArchivo()
        hash_chk = da.arch_hash(upload, \
                                hash_algorithm=HashAlgorithm,\
                                accelerate=AccelerateHash)
        print (" Applied ", HashAlgorithm, ":", hash_chk)

        aux = os.path.join(UploadFolder, filename)
        if utils.Ea.AgregarArchivo(aux, hash_chk, upload) != 0:
            no_agregados.append(filename)
        else:
            agregados.append(filename)

    # retornando respuesta
    if len(agregados) == 0:
        return ajax_response("error", "No se han subido nuevos archivos")

    return json.dumps([{ 'status':'ok',\
                         'no_agregados': no_agregados,\
                         'agregados': agregados}], \
                      separators=(',',':'), indent=4)

def ajax_response(status, msg) :
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
    
    
