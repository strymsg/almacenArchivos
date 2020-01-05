# this file is part of "El Botadero"
# copyright Rodrigo Garcia 2018 <strysg@riseup.net>
# AGPL liberated.

import functools

from . import controller as co
from . import utils as u

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    send_file, jsonify
)

botaderoBp = Blueprint('botadero', __name__, url_prefix='')

# TODO: mover la sincronizacion a un lugar mas convencional
# u.sincronizarArchivos(ignorar=['gitkeep'])

@botaderoBp.route('/')
@botaderoBp.route('/<string:cat>/')
def categoriaView(cat='Misc'):
    print('categoria::::', cat)
    html_page = u.obtenerHtmlListado(categoria=cat)

    return html_page.html

# vistas de descargas
@botaderoBp.route('/almacen/<string:nombreArchivo>', defaults={ 'cat': 'Misc'})
@botaderoBp.route('/almacen/<string:cat>/<string:nombreArchivo>')
def descargaDesdeIndexView(cat, nombreArchivo):

    if not co.descargaPermitida(cat, nombreArchivo):
        return ('No permitido: '+cat+'/'+nombreArchivo)

    pathf = co.descargarArchivo(cat, nombreArchivo)
    print('Descargando:::', pathf)
    if pathf is None:
        return render_template("noExiste.html",
                               nombre=nombreArchivo,
                               esquemaColores=u.esquemaColoresRandom())
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

    hashedPassword = ''
    resultado = co.subirArchivo(cat, file, hashedPassword)

    if not isinstance(resultado, dict):
        # caso exitoso, se debe actualizar
        co.sincronizarArchivos()
        html_page = u.obtenerHtmlListado(categoria=cat)
        return html_page.html
    else:
        html_page = u.obtenerHtmlListado(categoria=cat)
        return html_page.html

# vista de subida de varios archivos
@botaderoBp.route('/<string:cat>/upload_file_a', methods=['GET', 'POST'])
def subidaArchivos(cat):
    print('⮉ request (multiple):', request.files.getlist("file"))
    if cat == '':
        cat = 'Misc'

    hashedPassword = ''
    exitosos = []
    erroneos = []

    for upload in request.files.getlist("file"):
        print('* filename', upload.filename)
        resultado = co.subirArchivo(cat, upload, hashedPassword)
        if not isinstance(resultado, dict):
            print('exitoso:', resultado.name)
            exitosos.append(resultado.name)
        else:
            print('errorneo:', str(resultado))
            erroneos.append(resultado)
    # actualizando
    if len(exitosos) > 0:
        co.sincronizarArchivos()
    # retornando respuesta
    print('exitosos', exitosos)
    print('erroneos', erroneos)
    return jsonify(exitosos=exitosos, erroneos=erroneos)
