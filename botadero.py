'''
Copyright (C) 2016 Rodrigo Garcia

This file is part of botadero.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
  
'''
#import os
from flask import Flask
from flask import render_template
from flask import request, redirect, send_from_directory
from flask import url_for
from werkzeug import secure_filename

from Estadisticas_Archivos import *
from datos_archivo import *

#cargar configuraciones del servidor
EstadisticaArchivos = EstadisticaArchivos('parametros.txt', False)
ParametrosServer = EstadisticaArchivos.Parametros

app = Flask(__name__)

@app.route('/')
def pag_principal():
    EstadisticaArchivos.Actualizar()
    return render_template("index.html") + ls_archivos()

''' Peticiones para descarga de archivos subidos
basado en:
http://nullege.com/codes/search/flask.send_from_directory

Aqui se puede agregar algun mecanismo para acumular estadisticas
'''
@app.route('/almacen/<filename>')
def donwload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, \
                               as_attachment=True)

''' Funcion para subir archivos 
Al hacer seleccionar el boton para subir archivos, se debe comprobar algunos
criterios para ser guardados:

- Tamanyo del archivo
De acuerdo a un parametro definido en `parametros.txt', si el archivo es mayor
que `SIZE_1' y menor que `SIZE_2' (bytes) sera borrado en `TIME_TO_DEL_1' (dias)
,si es mayor que `SIZE_2' se borrara en `TIME_TO_DEL_2' donde se asume que
`SIZE_2' > `SIZE_1'.

- Si ya existe
Al tratar de subir el archivo y para ahorrar espacio de almacenamiento, se 
comprueba si el archivo ya existe. Esto haciendo un sha1sum del archivo enviado
por el usuario. Luego se busca en si este sha1sum coincide con el de algun
otro archivo.

Si el archivo ya existe, se muestra un mensaje al usuario:
"El archivo ya existe, pero puede que tenga otro nombre"
Y no se guarda en disco duro.

- Si hay espacio disponible
De `parametros.txt' se comprueba `TOTAL_STORAGE', si la suma de el tamanyo de
todos los archivos subidos mas el nuevo archivo exceden este valor, se muestra:

"No hay espacio disponible, Si quieres que haya mas puedes colaborar donando :)"

Si no se guarda en disco duro.
'''     
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file'] #devuelve tipo FileStorage
        filename = ''
        if file:
            filename = secure_filename(file.filename)

            # TODO: Ver la forma de hacer el checksum a medida
            # los datos van llegando con haslib.update() para no
            # copiar el archivo (duplicacion)
            
            sha1sum = hashlib.sha1(file.read()).hexdigest()
            print "[UPLOAD] - Request to upload File %s" %filename,\
                "checksum %s" % sha1sum

            # comprobar si el archivo ya existe, si no registrar
            # ...

            # restaura el puntero
            file.seek(0)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
            pag_res = render_template("index.html")

        return redirect("/", code=302)
        # http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    else:
        return "Aaah?"


''' Lista los archivos subidos y muestra detalles
Se muestran primero los mas recientes subidos
'''
def ls_archivos():
    # aqui usar la clase EstadisticaArchivos para cargar parametros
    #
    #
    
    # Lo siguiente es solo para pruebas
    # TODO: usar motor de templates jinja2, y usar tablas para mostar la
    #       lista de archivos adecuadamente.
    
    cad = '''
    <html> 
    <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
     <title>Archivador temporal para compartir archivos</title>
     <link rel="stylesheet" href="../static/base.css" type="text/css" />
    </head>
    <body>
'''
    cad = cad + '<div id="lista_archivos">'
    cad = cad + "<ul>"
    upload_folder = "almacen/"

    try:
        nombres = os.listdir(upload_folder)
    except OSError:
        pass
    else:
        for arch in nombres:

            # archivo
            cad = cad + '<dl> <a href="%(up)s%(arch)s"> %(arch)s </a>' % \
                  {"up": upload_folder,  "arch": arch}

            size_long = os.stat(upload_folder + arch).st_size
            unidades = "(B)"
            if size_long > 1000 and size_long < 1000000:
                tam = round(size_long/float(1000), 2)
                unidades = "(KB)"
            elif size_long > 1000000 and size_long < 1000000000:
                tam = round(size_long/float(1000000), 2)
                unidades = "(MB)"
            elif size_long > 1000000000:
                tam = round(size_long/float(1000000000), 2)
                unidades = "(GB)"
            else:
                tam = float(size_long)

            cad = cad + " <---------> " + str(tam) + " " + unidades
            cad = cad + " <b> N dias </b>"
            cad = cad + "</dl> \n"
    cad = cad + "</ul>"
    cad = cad + "</body> </html>"
    return cad


##### principal #####
if __name__ == '__main__':

    # cargar configuraciones del servidor
    

    print "[PARAMETERS] - TOTAL_STORAGE=%d" %ParametrosServer.TotalStorage
    print "[PARAMETERS] - UPLOAD_FOLDER=%s" %ParametrosServer.UploadFolder
    print "[PARAMETERS] - SIZE_1=%d" %ParametrosServer.Size1
    print "[PARAMETERS] - SIZE_2=%d" %ParametrosServer.Size2
    print "[PARAMETERS] - TO_DEL_1=%d" %ParametrosServer.TimeToDel1
    print "[PARAMETERS] - TIME_TO_DEL_2=%d" %ParametrosServer.TimeToDel2
    print "[PARAMETERS] - SIZE_MAX_TO_UPLOAD=%d" %ParametrosServer.SizeMaxToUpload
    print "[PARAMETERS] - Log File =%s" %ParametrosServer.LogFileName
    print "[PARAMETERS] - Debug Level =%d" %ParametrosServer.DebugLevel
    app.config['UPLOAD_FOLDER'] = ParametrosServer.UploadFolder
    #app.config['MAX_CONTENT_LENGTH'] = ParametrosServer.SizeMaxToUpload

    app.debug = True



    app.run()
