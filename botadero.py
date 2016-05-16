'''
Botadero, una aplicacion para compartir archivos libremente.
Copyright (C) 2016 Rodrigo Garcia <strysg@riseup.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from flask import Flask
from flask import render_template
from flask import request, redirect, send_from_directory
from flask import url_for

from werkzeug import secure_filename
from jinja2 import Environment, PackageLoader

from Estadisticas_Archivos import *
from datos_archivo import *
import random

# cargar configuraciones del servidor
EstadisticaArchivos = EstadisticaArchivos('parametros.txt', False)
ParametrosServer = EstadisticaArchivos.Parametros

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ParametrosServer.UploadFolder

# Develve el nombre de un esquema de colores al azar
def esquema_colores_random():
    # esquemas de colores definidos en static/
    esquemas = ('neutral', 'verde1', 'azul1', 'amarillo1',\
                'rojo1', 'cafe1')
    return esquemas[random.randint(0, len(esquemas)-1)]

##### Rutas #######
@app.route('/')
def pag_principal():
    EstadisticaArchivos.Actualizar()
    return render_template("index.html", \
                           borrar_1=EstadisticaArchivos.Parametros.TimeToDel0,\
                           borrar_2=EstadisticaArchivos.Parametros.TimeToDel2,\
                           esp_disp=EstadisticaArchivos.AlmacenDisponible/1000000,\
                           p_disp=EstadisticaArchivos.PorcentajeAlmacenDisponible,\
                           num_arch=EstadisticaArchivos.NumArchivos,\
                           lista_archivos=ls_archivos(),\
                           esquema_colores=esquema_colores_random())

''' Peticiones para descarga de archivos subidos
basado en:
http://nullege.com/codes/search/flask.send_from_directory

Aqui se puede agregar algun mecanismo para acumular estadisticas
'''
@app.route('/almacen/<filename>')
def donwload_file(filename):
    # TODO: excepcion si el archivo no existe
    EstadisticaArchivos.IncrementarNumDescargas(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, \
                               as_attachment=True)

''' Funcion para subir archivos '''
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # TODO: agregar captcha?
    if request.method == 'POST':
        file = request.files['file'] #devuelve tipo FileStorage
        filename = ''
        if file:
            filename = secure_filename(file.filename)

            # TODO: Ver la forma de hacer el checksum a medida
            # los datos van llegando con haslib.update() para no
            # copiar el archivo (evitar duplicacion)
            da = DatosDeArchivo()
            sha1sum = da.arch_sha1sum(file)
            #sha1sum = hashlib.sha1(file.read()).hexdigest()
            print "[UPLOAD] - Request to upload File %s" %filename\
                ,"            checksum %s" % sha1sum
            
            # restaura el puntero
            file.seek(0)
            aux = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if EstadisticaArchivos.AgregarArchivo(aux, sha1sum, file) != 0:
                # mostrar error en pantalla
                return mostrar_err_archivo_duplicado(sha1sum=sha1sum, nombre=filename)
                #return redirect('/estadisticas', code=302)

        return redirect("/", code=302)
        # http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    else:
        return "Aaah?"

@app.route('/estadisticas')
def mostrar_estadisticas():
    EstadisticaArchivos.Actualizar()

    return render_template("estadisticas.html", \
                           datos_archivos=EstadisticaArchivos.PilaArchivos,\
                           esp_disp=EstadisticaArchivos.AlmacenDisponible/1000000,\
                           p_disp=EstadisticaArchivos.PorcentajeAlmacenDisponible,\
                           num_arch=EstadisticaArchivos.NumArchivos,\
                           esquema_colores=esquema_colores_random())

@app.route('/info')
def mostar_info():
    return render_template("info.html", dm=EstadisticaArchivos.Parametros.TotalStorage/1000000,\
                           sz1=EstadisticaArchivos.Parametros.Size1/1000000,\
                           sz2=EstadisticaArchivos.Parametros.Size2/1000000,\
                           td0=EstadisticaArchivos.Parametros.TimeToDel0,\
                           td1=EstadisticaArchivos.Parametros.TimeToDel1,\
                           td2=EstadisticaArchivos.Parametros.TimeToDel2,\
                           ms=EstadisticaArchivos.Parametros.SizeMaxToUpload/1000000,\
                           esquema_colores=esquema_colores_random())

@app.route('/duplicado')
def mostrar_err_archivo_duplicado(sha1sum=None, nombre=None):
    return render_template("duplicado.html", sha1sum=sha1sum, nombre=nombre,\
                           esquema_colores=esquema_colores_random())

######## Funciones Misc ##########
# Devuelve una lista con nombre_archivo, tamanyo y dias_restantes 
# para eliminacion del directorio del de subidas.
def ls_archivos():
    # TODO: usar motor de templates jinja2, y usar tablas para mostar la
    #       lista de archivos adecuadamente.
    l_archivos = []
    
    upload_folder = ParametrosServer.UploadFolder
    pila_archivos = EstadisticaArchivos.PilaArchivos
    dias_restantes = EstadisticaArchivos.PilaDiasRestantes
    # para mostrar los mas recientes primero
    #pila_archivos.reverse()
    
    raw_nombres = []
    for ra in pila_archivos:
        raw_nombres.append(ra.Nombre)

    nombres = []
    # quitar la carpeta de los nombres
    for nomb in raw_nombres:
        #nombres.append(nomb)
        nombres.append(nomb[len(ParametrosServer.UploadFolder)+1 :])
    
    # coloca cada archivo en la pantalla
    i = 0
    for arch in nombres:
        # TODO: controlar excepcion
        size_long = pila_archivos[i].Tam
        unidades = "B"
        if size_long > 1000 and size_long < 1000000:
            tam = round(size_long/float(1000), 2)
            unidades = "KB"
        elif size_long > 1000000 and size_long < 1000000000:
            tam = round(size_long/float(1000000), 2)
            unidades = "MB"
        elif size_long > 1000000000:
            tam = round(size_long/float(1000000000), 2)
            unidades = "GB"
        else:
            tam = float(size_long)

        # lista a devolver
        l_archivos.append([upload_folder, arch, str(tam)+" "+unidades, \
                           str(dias_restantes[i])])

        i = i + 1

    return l_archivos



############## principal ########################
if __name__ == '__main__':

    #app.run(host='0.0.0.0')

    # cargar configuraciones del servidor
    EstadisticaArchivos.Inicializar()
    
    print "[PARAMETERS] - TOTAL_STORAGE=%d" %ParametrosServer.TotalStorage
    print "[PARAMETERS] - UPLOAD_FOLDER=%s" %ParametrosServer.UploadFolder
    print "[PARAMETERS] - SIZE_1=%d" %ParametrosServer.Size1
    print "[PARAMETERS] - SIZE_2=%d" %ParametrosServer.Size2
    print "[PARAMETERS] - TIME_TO_DEL_0=%d" %ParametrosServer.TimeToDel0
    print "[PARAMETERS] - TIME_TO_DEL_1=%d" %ParametrosServer.TimeToDel1
    print "[PARAMETERS] - TIME_TO_DEL_2=%d" %ParametrosServer.TimeToDel2
    print "[PARAMETERS] - SIZE_MAX_TO_UPLOAD=%d" %ParametrosServer.SizeMaxToUpload
    print "[PARAMETERS] - Log File =%s" %ParametrosServer.LogFileName
    print "[PARAMETERS] - Debug Level =%d" %ParametrosServer.DebugLevel


    #app.debug = True # cuidado con esto a la hora de poner en produccion!

    app.run(host='0.0.0.0')
