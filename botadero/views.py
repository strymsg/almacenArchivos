# this file is part of "El Botadero"
# copyright Rodrigo Garcia 2018 <strysg@riseup.net>
# AGPL liberated.

import functools

from . import controller as co
from . import utils as u

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    send_file
)

botaderoBp = Blueprint('botadero', __name__, url_prefix='')

# TODO: mover la sincronizacion a un lugar mas convencional
u.sincronizarArchivos(ignorar=['gitkeep'])

@botaderoBp.route('/', defaults={ 'cat':'Misc' })
@botaderoBp.route('/<string:cat>/')
def categoriaView(cat):
    co.comprobarTiempoBorradoListaArchivos(cat)
    
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
    #return (str(cat+'/'+nombreArchivo))

# vista de subida de archivos
# @botaderoBp.route('/almacen/<string:cat>/upload', defaults={ 'cat': 'Misc' })
# @botaderoBp.route('/almacen/upload')
# def subidaArchivos(cat, nombreArchivo):
    
