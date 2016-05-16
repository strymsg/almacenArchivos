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
import os, sys, datetime, hashlib

class DatosDeArchivo:
    Nombre = ''
    Tam = 0
    FechaYHoraDeSubida = datetime.datetime.now()
    Extension = ''
    NumDescargas = 0
    sha1sum = ''

    def __init__(self):
        self.Nombre = ''
        self.Tam = 0
        self.FechaYHoraDeSubida = datetime.datetime.now()
        self.Extension = ''
        self.NumDescargas = 0
        self.sha1sum = ''

    def auto_init(self, Nombre_con_ruta):
        self.Nombre = Nombre_con_ruta
        ## determinacion de atributos
        # tamanyo
        self.Tam = os.stat(Nombre_con_ruta).st_size
        # Extension
        self.Extension = ''
        if len(Nombre_con_ruta.rsplit('.', 1)) > 1:
            self.Extension = Nombre_con_ruta.rsplit('.', 1 )[1]
        # NumDescargas
        self.NumDescargas = 0
        # sha1sum
        self.sha1sum = ''
        with open(self.Nombre, 'r') as fil:
            self.sha1sum = self.arch_sha1sum(fil)
        # Fecha y hora simula creacion del archivo ahora.
        self.FechaYHoraDeSubida = datetime.datetime.now()

    # Recibe un objeto archivo y devulve el sha1sum
    # Nota: No se restaura el puntero ni se cierra el archivo
    def arch_sha1sum(self, archivo):
        archivo.seek(0) # puntero en 0
        t_ant = -1
        t_act = archivo.tell()
        pedazo_tam = 125*1024
        h = hashlib.sha1()
        # obtiene el sha1sum del archivo por pedazos de 125 MB a lo maximo
        # esto la hace en caso de ser un archivo con tamanyo mas grande que 2GB
        # por ser su contenido mayor que el maximo de una cadena (2^32)
        while t_ant != t_act: 
            cad = archivo.read(pedazo_tam)
            h.update(cad)
            t_ant = t_act
            t_act = archivo.tell()
        return h.hexdigest()

# Nota acerca del nombre del archivo
#  espcificar el archivo con la ruta completa
# ejemplo para obtener ruta segura:
#     ruta = almacen  ,  nombre = tatoo.png
# se puede crear de forma segura con:
#     DatosArchivo = DatosDeArchivo(os.path.join(ruta, nombre))

    def edad(self):
        return (datetime.datetime.now() - self.FechaYHoraDeSubida).days
        #return (datetime.datetime.now() - self.FechaYHoraDeSubida).seconds










'''
Notas:

sha1sum
  >>> import hashlib
  >>> hashlib.sha1("123").hexdigest
  40bd001563085fc35165329ea1ff5c5ecbdbbeef

datetime

  Para obtener la diferencia de dias entre un datetime guardado antes y 
  el datetime acutal

  >>> d1 = datetime.datetime.now()
  >>> d1
  datetime.datetime(2016, 3, 21, 16, 45, 33, 676366)

  Para los dias
  >>> (datetime.datetime.now() - d1).days
  0
  Segundos
  >>> (datetime.datetime.now() - d1).seconds
  70

  >>> datetime.datetime.now()
  datetime.datetime(2016, 3, 21, 16, 25, 19, 192717)

  >>> d = datetime.datetime.now()
  >>> d.hour
  16
  >>> d.second
  47
  >>> d.minute
  25
  ...

tamanyo 
  >>> import os
  >>> os.stat("libreboot").st_size
  12788L

'''

    
        
        
