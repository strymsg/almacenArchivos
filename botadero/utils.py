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
from botadero.Estadisticas_Archivos import *
from botadero.datos_archivo import *
import random

EstadisticaArchivos = EstadisticaArchivos('parametros.txt', False)
ParametrosServer = EstadisticaArchivos.Parametros

# Develve el nombre de un esquema de colores al azar
def esquema_colores_random():
    '''
    devuelve un esquema de colores random de los definidos en static/
    '''
    esquemas = ('gris1', 'neutral','verde1','azul1','amarillo1', 'rojo1','cafe1')

    return esquemas[random.randint(0, len(esquemas)-1)]

def ls_archivos(categoria=""):
    '''
    Devuelve una lista con nombre_archivo, tamanyo y dias_restantes 
    para eliminacion del directorio de subidas.
    '''
    l_archivos = []
    
    upload_folder = ParametrosServer.UploadFolder
    pila_archivos = EstadisticaArchivos.PilaArchivos

    nombres = []
    for ra in pila_archivos:
        if ra.categoria == categoria:
            nombres.append(ra.Nombre)

    # coloca cada archivo en la pantalla
    for arch in nombres:
        # TODO: controlar excepcion
        size_long = EstadisticaArchivos.GetDatosArchivo(arch).Tam
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
                           str(EstadisticaArchivos.GetDatosArchivo(arch).DiasRestantes)])

    return l_archivos

def categorias():
    '''
    Devuelve la lista categorias (carpetas) dentro el directorio almacen/
    No realiza recursion solo devuelve carpetas en el nivel 1
    '''
    upload_folder = ParametrosServer.UploadFolder
    pathf = os.path.abspath(upload_folder)
    #print "[DIRS] - abs path: %s" %pathf
    
    categorias = []
    ow = os.walk(pathf) # apuntando a /alamacen
    # por el momento solo se hace la comprobacion de un nivel
    directorios = ow.next()[1]
    for d in directorios:
        categorias.append(d)
    print "[DIRS] - folders found: %s" %str(directorios)
    
    return categorias
    #print "[DIRS] - List of folders: %s" %filter(os.path.isdir, os.listdir(pathf))
    #return filter(os.path.isdir, os.listdir(pathf))

def num_archivos_por_categoria(categoria):
    '''Devuelve el numero de archivos segun la categoria
    dada'''
    num = 0
    for da in EstadisticaArchivos.PilaArchivos:
        if da.categoria == categoria:
           num += 1
    return num

def categorias_y_nums_archivos():
    '''Devuelve una lista con (categria, num_archivos)
    de cada categoria de archivos'''
    cats = []
    cats.append("") # para el directorio principal
    cats = cats + categorias()
    cat_y_nums = []
    for cat in cats:
        cat_y_nums.append((cat, num_archivos_por_categoria(cat)))

    return cat_y_nums
    


    
