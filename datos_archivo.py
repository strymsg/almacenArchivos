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
            self.sha1sum = hashlib.sha1(fil.read()).hexdigest()
        # Fecha y hora simula creacion del archivo ahora.
        self.FechaYHoraDeSubida = datetime.datetime.now()

# Nota acerca del nombre del archivo
#  espcificar el archivo con la ruta completa
# ejemplo para obtener ruta segura:
#     ruta = almacen  ,  nombre = tatoo.png
# se puede crear de forma segura con:
#     DatosArchivo = DatosDeArchivo(os.path.join(ruta, nombre))

    # def __init__(self, Nombre_con_ruta, Tam, FechaYHoraDeSubida, Extension, sha1sum):
    #     self.Nombre = Nombre_con_ruta
    #     self.Tam = Tam
    #     self.FechaYHoraDeSubida = FechaYHoraDeSubida
    #     self.Extension = Extension
    #     self.NumDescargas = 0
    #     self.sha1sum = sha1sum

    def dias_restantes(self):
        return (datetime.datetime.now() - self.FechaYHoraDeSubida).days()










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

    
        
        
