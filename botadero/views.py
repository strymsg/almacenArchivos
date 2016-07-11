'''
This file is part of Botadero
'''
from botadero import app
from botadero import utils

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
    utils.EstadisticaArchivos.Actualizar()
    #categorias = ['Misc.', 'Musica', 'documentos', 'videos']
    categoria_actual = ''
    categorias_con_nums = utils.categorias_y_nums_archivos()

    return render_template("index.html", \
                           borrar_1=utils.EstadisticaArchivos.Parametros.TimeToDel0,\
                           borrar_2=utils.EstadisticaArchivos.Parametros.TimeToDel2,\
                           esp_disp=utils.EstadisticaArchivos.AlmacenDisponible/1000000,\
                           p_disp=utils.EstadisticaArchivos.PorcentajeAlmacenDisponible,\
                           num_arch=utils.EstadisticaArchivos.NumArchivos,\
                           lista_archivos=utils.ls_archivos(),\
                           esquema_colores=utils.esquema_colores_random(),\
                           categoria_actual=categoria_actual,\
                           categorias_con_nums=categorias_con_nums)

@app.route('/<cat>/')
def pag_principal(cat):
    utils.EstadisticaArchivos.Actualizar()
    categorias = utils.categorias()
    categoria_actual = ''
    if cat in categorias:
        categoria_actual = cat
    else:
        return cat # TODO: redirigir a pagina error en categoria

    categorias_con_nums = utils.categorias_y_nums_archivos()

    return render_template("index.html", \
                           borrar_1=utils.EstadisticaArchivos.Parametros.TimeToDel0,\
                           borrar_2=utils.EstadisticaArchivos.Parametros.TimeToDel2,\
                           esp_disp=utils.EstadisticaArchivos.AlmacenDisponible/1000000,\
                           p_disp=utils.EstadisticaArchivos.PorcentajeAlmacenDisponible,\
                           num_arch=utils.EstadisticaArchivos.NumArchivos,\
                           lista_archivos=utils.ls_archivos(categoria_actual),\
                           esquema_colores=utils.esquema_colores_random(),\
                           categoria_actual=categoria_actual,\
                           categorias_con_nums=categorias_con_nums)

@app.route('/estadisticas')
def mostrar_estadisticas():
    utils.EstadisticaArchivos.Actualizar()

    return render_template("estadisticas.html", \
                           datos_archivos=utils.EstadisticaArchivos.PilaArchivos,\
                           esp_disp=utils.EstadisticaArchivos.AlmacenDisponible/1000000,\
                           p_disp=utils.EstadisticaArchivos.PorcentajeAlmacenDisponible,\
                           num_arch=utils.EstadisticaArchivos.NumArchivos,\
                           esquema_colores=utils.esquema_colores_random())

@app.route('/info')
def mostar_info():
    return render_template("info.html", dm=utils.EstadisticaArchivos.Parametros.TotalStorage/1000000,\
                           sz1=utils.EstadisticaArchivos.Parametros.Size1/1000000,\
                           sz2=utils.EstadisticaArchivos.Parametros.Size2/1000000,\
                           td0=utils.EstadisticaArchivos.Parametros.TimeToDel0,\
                           td1=utils.EstadisticaArchivos.Parametros.TimeToDel1,\
                           td2=utils.EstadisticaArchivos.Parametros.TimeToDel2,\
                           ms=utils.EstadisticaArchivos.Parametros.SizeMaxToUpload/1000000,\
                           esquema_colores=utils.esquema_colores_random())

@app.route('/duplicado')
def mostrar_err_archivo_duplicado(sha1sum=None, nombre=None):
    return render_template("duplicado.html", sha1sum=sha1sum, nombre=nombre,\
                           esquema_colores=utils.esquema_colores_random())

