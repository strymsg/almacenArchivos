# this file is part of "El Botadero"
# copyright Rodrigo Garcia 2018 <strysg@riseup.net>
# AGPL liberated.

import functools

from . import controller as co
from . import utils as u

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    send_file, jsonify, make_response
)

botaderoBp = Blueprint('botadero', __name__, url_prefix='')

# TODO: mover la sincronizacion a un lugar mas convencional
# u.sincronizarArchivos(ignorar=['gitkeep'])

@botaderoBp.route('/')
@botaderoBp.route('/<string:cat>/')
def categoriaView(cat='Misc'):
    html_page = u.obtenerHtmlListado(categoria=cat)

    return html_page.html

# endpoint descarga 
@botaderoBp.route('/almacen/<string:cat>/<string:nombreArchivo>')
def descargaDesdeIndexView(cat, nombreArchivo):
    print('⏬ file:', cat, nombreArchivo)
    if not co.descargaPermitida(cat, nombreArchivo):
        return ('No permitido: '+cat+'/'+nombreArchivo), 404

    pathf = co.descargarArchivo(cat, nombreArchivo)
    if pathf is None:
        return render_template("noExiste.html",
                               nombre=nombreArchivo,
                               esquemaColores=u.esquemaColoresRandom()), 404
    return send_file(pathf, as_attachment=True)

# endpoint descarga protegida (ajax)
@botaderoBp.route('/<string:cat>/download_protected', methods=['GET', 'POST'])
def descargarArchivoProtegidoAjax(cat):
    nombreArchivo = request.form.get('nombre_archivo_protegido')
    print('⏬ ⚿ file', cat, nombreArchivo)
    if cat == '':
        cat = 'Misc'
    resultados = {}
    if 'pwd_archivo' not in request.form or \
       'nombre_archivo_protegido' not in request.form:
        resultados = {
            'error': {
                'msj': 'No se han proporcionado datos completos',
                'code': 1
            }
        }
        return make_response(jsonify(resultados), 400)
    password = request.form.get('pwd_archivo')
    if not co.descargaPermitida(cat, nombreArchivo):
        resultados = {
            'error': {
                'msj': 'Descarga no permitida',
                'code': 3
            }
        }
        return make_response(jsonify(resultados), 401)
    pathf = co.descargarArchivo(cat, nombreArchivo, password=password)
    if isinstance(pathf, dict):
        resultados = {
            'error': {
                'msj': pathf['mensaje'],
                'code': pathf['tipoError']
            }
        }
        return make_response(jsonify(resultados), 403)
    return send_file(pathf, as_attachment=True)
    
# vista de subida de archivo (individual) este caso se asume que no se usa javascript.
@botaderoBp.route('/<string:cat>/upload_file', methods=['GET', 'POST'])
def subidaArchivo(cat):
    print('⮉ request (individual)', request.files.get('file', 'No se ha proporcionado archivo'), ', method=', request.method, 'categoria=', cat)
    if cat == '':
        cat = 'Misc'
    if 'file' not in request.files:
        return 'Debe subir un archivo'
    file = request.files['file']
    if file.filename == '':
        html_page = u.obtenerHtmlListado(categoria=cat)
        return html_page.html

    resultado = {}
    if request.form.get('password') is not None:
        resultado = co.subirArchivo(cat, file, request.form.get('password'))
    else:
        resultado = co.subirArchivo(cat, file)

    if not isinstance(resultado, dict):
        # caso exitoso, se debe actualizar
        co.sincronizarArchivos("['.gitkeep', '.gitkeep~', '#.gitkeep', '#.gitkeep#']")
        html_page = u.obtenerHtmlListado(categoria=cat)
        return redirect("/"+cat, code=302)
    else:
        html_page = u.obtenerHtmlListado(categoria=cat)
        return redirect("/"+cat, code=302)

# vista de subida de varios archivos
@botaderoBp.route('/<string:cat>/upload_file_a', methods=['GET', 'POST'])
def subidaArchivos(cat):
    print('⮉ request (multiple):', request.files.getlist("file"))
    if cat == '':
        cat = 'Misc'

    password = ''
    if request.form.get('password') is not None:
        password = request.form.get('password')
    exitosos = []
    erroneos = []

    for upload in request.files.getlist("file"):
        print('* filename', upload.filename)
        resultado = None
        if password != '':
            resultado = co.subirArchivo(cat, upload, password)
        else:
            resultado = co.subirArchivo(cat, upload)
        if not isinstance(resultado, dict):
            print('exitoso:', resultado.name)
            exitosos.append(resultado.name)
        else:
            print('errorneo:', str(resultado))
            erroneos.append(resultado)
    # actualizando
    if len(exitosos) > 0:
        co.sincronizarArchivos("['.gitkeep', '.gitkeep~', '#.gitkeep', '#.gitkeep#']")
        co.marcarTodasLasPaginasParaRenderizar()
    # retornando respuesta
    print('exitosos', exitosos)
    print('erroneos', erroneos)
    return jsonify(exitosos=exitosos, erroneos=erroneos)
