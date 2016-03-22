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
'''
'''
class DatosDeArchivo:
    def __init__(self):
        self.Nombre = ''
        self.Tam = 0
        self.FechaYHoraDeSubida = datetime.datetime.now()
        self.Extension = ''
        self.NumDescargas = 0
        self.sha1sum = ''

    def __init__(Nombre, Tam, FechaYHoraDeSubida, Extension, NumDescargas,\
                 sha1sum):
        self.Nombre = Nombre
        self.Tam = Tam
        self.FechaYHoraDeSubida = FechaYHoraDeSubida
        self.Extension = Extension
        self.NumDescargas = NumDescargas
        self.sha1sum = sha1sum

    # constructor inteligente
    # deberia determinar todos los demas atributos automaticamente
    def __init__(Nombre):
        self.Nombre = Nombre


    def dias_restantes(self):
        return (datetime.datetime.now() - FechaYHoraDeSubida).days()

    

'''
Notas:

sha1sum

  >>>hashlib.sha1("123").hexdigest
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

'''

    
        
        
