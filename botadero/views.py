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

log = g.log

botaderoBp = Blueprint('botadero', __name__, url_prefix='')

@botaderoBp.route('/')
@botaderoBp.route('/<string:cat>/')
def categoriaView(cat='Misc'):
    html_page = u.obtenerHtmlListado(categoria=cat)
    return html_page.html

# endpoint descarga 
@botaderoBp.route('/almacen/<string:cat>/<string:nombreArchivo>')
def descargaDesdeIndexView(cat, nombreArchivo):
    log.info('⏬ file: {0} {1}'.format(cat, nombreArchivo))
    if not co.descargaPermitida(cat, nombreArchivo):
        return ('No permitido: '+cat+'/'+nombreArchivo), 404

    if co.tienePassword(nombreArchivo):
        # TODO: redirect a descarga con password
        return ('No permitido tiene password: '+cat+'/'+nombreArchivo), 404
    
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
    log.info('⏬ ⚿ file {0}: {1}'.format(cat, nombreArchivo))
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
    if not co.tienePassword(nombreArchivo):
        resultados = {
            'error': {
                'msj': 'Este archivo no requiere contraseña',
                'code': 4
            }
        }
        return make_response(jsonify(resultados), 401)
    if len(password) < 2:
        resultados = {
            'error': {
                'msj': 'Contraseña incorrecta',
                'code': 2
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

# formulario de descarga para archivos protegidos
@botaderoBp.route('/almacen/<string:cat>/<string:nombreArchivo>/descargar_protegido', methods=['GET'])
def descargarArchivoProtegidoForm(cat, nombreArchivo):
    log.info('☱ download file protected (form): categoria={0}, nombre={1}'
                    , cat, nombreArchivo)
    if cat == '':
        cat = 'Misc'
    if not co.descargaPermitida(cat, nombreArchivo):
        return ('No permitido: '+cat+'/'+nombreArchivo), 404

    pathf = co.descargarArchivo(cat, nombreArchivo)
    if pathf is None:
        return render_template("noExiste.html",
                               nombre=nombreArchivo,
                               esquemaColores=u.esquemaColoresRandom()), 404
    if not co.tienePassword(nombreArchivo):
        return render_template("noExiste.html",
                               nombre=nombreArchivo,
                               esquemaColores=u.esquemaColoresRandom()), 404
    return u.renderizarHtmlArchivoProtegido(cat, nombreArchivo)
    
# vista de subida de archivo (individual) este caso se asume que no se usa javascript.
@botaderoBp.route('/<string:cat>/upload_file', methods=['GET', 'POST'])
def subidaArchivo(cat):
    # La siguiente línea es para evitar el error con uwsgi
    # *4719 readv() failed (104: Connection reset by peer) while reading upstream
    # Ref: https://uwsgi.readthedocs.io/en/latest/ThingsToKnow.html?highlight=clobbered
    rdata = request.get_data(cache=True)

    log.info('⮉ request (individual): name={0}, method={1}, categoria={2}'
                    .format(
                        request.files.get('file', 'No se ha proporcionado archivo'), \
                        request.method, cat))
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
        co.marcarTodasLasPaginasParaRenderizar()
        html_page = u.obtenerHtmlListado(categoria=cat)
        return redirect("/"+cat, code=302)
    else:
        html_page = u.obtenerHtmlListado(categoria=cat)
        return redirect("/"+cat, code=302)

# vista de subida de varios archivos
@botaderoBp.route('/<string:cat>/upload_file_a', methods=['GET', 'POST'])
def subidaArchivos(cat):
    # La siguiente línea es para evitar el error con uwsgi
    # *4719 readv() failed (104: Connection reset by peer) while reading upstream
    # Ref: https://uwsgi.readthedocs.io/en/latest/ThingsToKnow.html?highlight=clobbered
    rdata = request.get_data(cache=True)
    # log.warning('request.data?::::\n{0}\n::::::::'.format(len(rdata)))

    log.info('⮉ request (multiple): files={0}'.format(request.files.getlist("file")))
    if cat == '':
        cat = 'Misc'

    password = ''
    if request.form.get('password') is not None:
        password = request.form.get('password')
    exitosos = []
    erroneos = []

    # TODO: controlar suma de peticion y tamaño máximo
    # ...
    
    for upload in request.files.getlist("file"):
        log.debug('* filename {0}'.format(upload.filename))
        resultado = None
        if password != '':
            resultado = co.subirArchivo(cat, upload, password)
        else:
            resultado = co.subirArchivo(cat, upload)
        if not isinstance(resultado, dict):
            log.debug('exitoso: {0}'.format(resultado.name))
            exitosos.append(resultado.name)
        else:
            log.debug('errorneo: {0}'.format(str(resultado)))
            erroneos.append(resultado)
    # actualizando
    if len(exitosos) > 0:
        co.sincronizarArchivos("['.gitkeep', '.gitkeep~', '#.gitkeep', '#.gitkeep#']")
        co.marcarTodasLasPaginasParaRenderizar()
    # retornando respuesta
    log.debug('exitosos:\n {0}'.format(str(exitosos)))
    log.debug('erroneos:\n {0}'.format(str(erroneos)))
    return jsonify(exitosos=exitosos, erroneos=erroneos)

####### vistas informativas ######

@botaderoBp.route('/info', methods=['GET'])
def info_page():
    html_page = u.obtener_pag_info()
    return html_page.html

