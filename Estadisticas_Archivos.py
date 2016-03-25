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
import hashlib
from Parametros_Servidor import *
from datos_archivo import *

class EstadisticaArchivos:
    def __init__(self, NombreArchivoConfig, DebugLevel):
        self.Parametros = ParametrosServidor(NombreArchivoConfig \
                                             , DebugLevel)
        self.AlmacenDisponible = 0
        self.PorcentajeAlmacenDisponible = 0
        self.NumArchivos = 0
        
        self.DictArchivos = {'', DatosDeArchivo} # dummy
        #self.init(self)

    def ExisteNombre(self,Nombre_con_ruta):
        if Nombre_con_ruta in DictArchivos:
            return True
        else:
            return False
            

    def ExisteArchivo(self, Nombre_con_ruta, sha1sum):
        if ExisteNombre(Nombre_con_ruta):
            if sha1sum == DictArchivos[NombreArchivo].sha1sum:
                return True
            else:
                return False
        else:
            return False
        

    def AgregarArchivo(self, Nombre_con_ruta, tam, \
                       FechaYHoraDeSubida, Extension, sha1sum):
        
        if ExisteArchivo(Nombre_con_ruta, sha1sum):
            print "[STORE] - Warn: File %s " % Nombre_con_ruta, \
                "or sha1sum %s exists, not uploaded." %sha1sum
            return 1
        else:
            # agrega el nuevo a las estadisticas
            self.DictArchivos[Nombre_con_ruta] = \
                DatosDeArchivo(Nombre_con_ruta, tam, \
                               FechaYHoraDeSubida, Extension,sha1sum)
            
