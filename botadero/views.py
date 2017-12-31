'''
This file is part of Botadero
'''
from botadero import app
from botadero import utils
#from botadero.utils import *

from flask import Blueprint
from flask import render_template
from flask import request, redirect, send_from_directory, safe_join, send_file
from flask import url_for

from werkzeug import secure_filename
from jinja2 import Environment, PackageLoader

import os

##### Rutas #######
@app.route('/')
def pag_inicio():
    utils.Ea.Actualizar()
    #utils.EstadisticaArchivos.MostrarRegistros()
    #categorias = ['Misc.', 'Musica', 'documentos', 'videos']
    categoria_actual = ''
    categorias_con_nums = utils.categorias_y_nums_archivos()

    return render_template("index.html", \
                           borrar_1=utils.Ea.Parametros.TimeToDel0,\
                           borrar_2=utils.Ea.Parametros.TimeToDel2,\
                           esp_disp=utils.Ea.almacenDisponible/1000000,\
                           p_disp=utils.Ea.porcentajeAlmacenDisponible,\
                           num_arch=utils.Ea.numArchivos,\
                           lista_archivos=utils.ls_archivos(),\
                           esquema_colores=utils.esquema_colores_random(),\
                           categoria_actual=categoria_actual,\
                           categorias_con_nums=categorias_con_nums,\
                           ms=utils.Ea.Parametros.SizeMaxToUpload)

@app.route('/<cat>/')
def pag_principal(cat):
    utils.Ea.Actualizar()
    categorias = utils.categorias()
    categoria_actual = ''
    if cat in categorias:
        categoria_actual = cat
    else:
        return cat # TODO: redirigir a pagina error en categoria

    categorias_con_nums = utils.categorias_y_nums_archivos()

    return render_template("index.html", \
                           borrar_1=utils.Ea.Parametros.TimeToDel0,\
                           borrar_2=utils.Ea.Parametros.TimeToDel2,\
                           esp_disp=utils.Ea.almacenDisponible/1000000,\
                           p_disp=utils.Ea.porcentajeAlmacenDisponible,\
                           num_arch=utils.Ea.numArchivos,\
                           lista_archivos=utils.ls_archivos(categoria_actual),\
                           esquema_colores=utils.esquema_colores_random(),\
                           categoria_actual=categoria_actual,\
                           categorias_con_nums=categorias_con_nums,\
                           ms=utils.Ea.Parametros.SizeMaxToUpload)

@app.route('/estadisticas')
def mostrar_estadisticas():
    utils.Ea.Actualizar()

    return render_template("estadisticas.html", \
                           datos_archivos=utils.Ea.PilaArchivos,\
                           esp_disp=utils.Ea.almacenDisponible/1000000,\
                           p_disp=utils.Ea.porcentajeAlmacenDisponible,\
                           num_arch=utils.Ea.numArchivos,\
                           esquema_colores=utils.esquema_colores_random())

@app.route('/info')
def mostar_info():
    return render_template("info.html", dm=utils.Ea.Parametros.TotalStorage/1000000,\
                           sz1=utils.Ea.Parametros.Size1/1000000,\
                           sz2=utils.Ea.Parametros.Size2/1000000,\
                           td0=utils.Ea.Parametros.TimeToDel0,\
                           td1=utils.Ea.Parametros.TimeToDel1,\
                           td2=utils.Ea.Parametros.TimeToDel2,\
                           ms=utils.Ea.Parametros.SizeMaxToUpload/1000000,\
                           esquema_colores=utils.esquema_colores_random())

@app.route('/duplicado')
def mostrar_err_archivo_duplicado(hash_check=None, nombre=None):
    return render_template("duplicado.html", hash_check=hash_check, nombre=nombre,\
                           esquema_colores=utils.esquema_colores_random())

