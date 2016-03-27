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
from Parametros_Servidor import *
from datos_archivo import *

class EstadisticaArchivos:
    def __init__(self, NombreArchivoConfig, DebugLevel):
        self.Parametros = ParametrosServidor(NombreArchivoConfig \
                                             , DebugLevel)
        self.AlmacenDisponible = 0
        self.PorcentajeAlmacenDisponible = 0
        self.NumArchivos = 0

        self.PilaArchivos = []
        #self.DictArchivos = {'': DatosDeArchivo} # dummy

    def GetDatosArchivo(self,  Nombre_con_ruta):
        for nombre in self.PilaArchivos:
            if Nombre_con_ruta == nombre:
                return self.PilaArchivos.index(Nombre_con_ruta)
        return None

    def ExisteNombre(self, Nombre_con_ruta):
        for da in self.PilaArchivos:
            if Nombre_con_ruta == da.Nombre:
                return True
        return False
            
    def ExisteArchivo(self, Nombre_con_ruta, sha1sum):
        if self.ExisteNombre(Nombre_con_ruta):
            if self.GetDatosArchivo(Nombre_con_ruta).sha1sum == \
                sha1sum:
                return True
            else:
                return False
        return False
        

    def AgregarArchivo(self, Nombre_con_ruta, tam, \
                       FechaYHoraDeSubida, Extension, sha1sum):
        # TODO: Agregar comprobacion de espacio disponible
        # ...
        if self.ExisteArchivo(Nombre_con_ruta, sha1sum):
            print "[STORE] - Warn: File %s " % Nombre_con_ruta, \
                "or sha1sum %s exists, not uploaded." %sha1sum
            return 1
        else:
            # agrega el nuevo registro a las estadisticas
            da = DatosDeArchivo(Nombre_con_ruta, tam, \
                                FechaYHoraDeSubida, Extension,sha1sum)
            self.PilaArchivos.append(da)
            return 0
            
    def BorrarArchivo(self, Nombre_con_ruta):
        if self.ExisteNombre(Nombre_con_ruta):
            # borra el archivo de disco
            os.remove(Nombre_con_ruta)
            # borra el registro del archivo del diccionario de registros
            del self.PilaArchivos[self.PilaArchivos.index(Nombre_con_ruta)]

    # comprueba si uno o mas archivos han estado almacenados por mas
    # dias de los especificados para su eliminacion.
    # Los elimina automaticamente y los borra del registro
    def ComprobarTiempoArchivos(self):
        archivos_a_borrar = []
        for da in self.PilaArchivos:
            dt = (datetime.datetime.now() - da.FechaYHoraDeSubida).days
            
            # tamanyo
            tamanyo = da.Tam
            if tamanyo > self.Parametros.Size1 and \
               tamanyo < self.Parametros.Size2:
                if dt >= self.Parametros.TimeToDel1:
                    archivos_a_borrar.append(da.Nombre) # marca para borrar
            elif tamanyo > self.Parametros.Size2:
                if  dt >= self.Parametros.TimeToDel2:
                    archivos_a_borrar.append(da.Nombre) # marca para borrar
            
        # borrado
        for na in archivos_a_borrar:
            # log
            print '[REG] - Delete: File %(na)s size %(sz)d'\
                  % {'na': na , 'sz': self.GetDatosArchivo(na).Tam} , \
                  'created at',\
                  self.GetDatosArchivo(na).FechaYHoraDeSubida , 'deleted!'
            self.BorrarArchivo(na)

    # comprueba las lista de archivos y si existen en el registro
    # crea nuevos registros si hay archivos nuevos.
    # Llama a la funcion ComprobarTiempoArchivos() para eliminar archivos
    # automaticamente segun `Parametros'
    def Actualizar(self):
        nombres = self.ArchOrdenadosFechaSubida(self.Parametros.UploadFolder)
        # comprueba si los archivos estan en los registros
        for nomb in nombres:
            self.GetDatosArchivo(nomb) 
            if self.ExisteNombre(nomb) == False:
                # actualizar registro del nuevo archivo 
                # este caso se deberia dar cuando se copia manualmente
                # archivos en la carpeta `UploadFolder'
                dt_arch = DatosDeArchivo()
                dt_arch.auto_init(nomb)
                # agrega nuevo registro
                self.PilaArchivos.append(dt_arch)
                    
                # log TODO: activar este log solo si `LOG_REG' (implementar)
                print '[REG] - New: File %(na)s size %(sz)d'\
                    % {'na': nomb , 'sz': self.PilaArchivos[-1].Tam},\
                    'created at', self.PilaArchivos[-1].FechaYHoraDeSubida

        self.ComprobarTiempoArchivos()

        # determinacion de otros parametros estadisticos
        tam_total = 0
        for da in self.PilaArchivos:
            tam_total = tam_total + da.Tam
            
        self.AlmacenDisponible = self.Parametros.TotalStorage - tam_total
        self.PorcentajeAlmacenDisponible = 100 - (tam_total * 100)\
                                           / self.AlmacenDisponible
        self.NumArchivos = len(self.PilaArchivos)

        # log
        print '[REG] - Updated.'
    

    def ArchOrdenadosFechaSubida(self, ruta):
        # fuente http://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python?lq=1
        files = filter(os.path.isfile, os.listdir(ruta))
        try:
            files = os.listdir(ruta)
        except OSError:
            pass
        else:
            files = [os.path.join(ruta, f) for f in files] # add path to each file
            files.sort(key=lambda x: os.path.getmtime(x)) 
        # queda ordenado con el archivo con mas antiguedad primero
        return files
