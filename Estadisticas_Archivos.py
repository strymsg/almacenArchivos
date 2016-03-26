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
        
        self.DictArchivos = {'': DatosDeArchivo} # dummy
        #self.DictArchivos = {}

    def ExisteNombre(self,Nombre_con_ruta):
        if Nombre_con_ruta in self.DictArchivos:
            return True
        else:
            return False
            

    def ExisteArchivo(self, Nombre_con_ruta, sha1sum):
        if self.ExisteNombre(Nombre_con_ruta):
            if sha1sum == DictArchivos[NombreArchivo].sha1sum:
                return True
            else:
                return False
        else:
            return False
        

    def AgregarArchivo(self, Nombre_con_ruta, tam, \
                       FechaYHoraDeSubida, Extension, sha1sum):
        
        if self.ExisteArchivo(Nombre_con_ruta, sha1sum):
            print "[STORE] - Warn: File %s " % Nombre_con_ruta, \
                "or sha1sum %s exists, not uploaded." %sha1sum
            return 1
        else:
            # agrega el nuevo a las estadisticas
            self.DictArchivos[Nombre_con_ruta] = \
                DatosDeArchivo(Nombre_con_ruta, tam, \
                               FechaYHoraDeSubida, Extension,sha1sum)
            
    def BorrarArchivo(self, Nombre_con_ruta):
        if self.ExisteNombre(Nombre_con_ruta):
            # borra el archivo de disco
            os.remove(Nombre_con_ruta)
            
            # borra el registro del archivo del diccionario de registros
            del[self.DictArchivos[Nombre_con_ruta]]

    # comprueba si uno o mas archivos han estado almacenados por mas
    # dias de los especificados para su eliminacion.
    # Los elimina automaticamente y los borra del registro
    def ComprobarTiempoArchivos(self):
        archivos_a_borrar = []
        for na, da in self.DictArchivos.iteritems():
            dt = datetime.datetime.now() - da.day
            
            # tamanyo
            tamanyo = da.Tam
            if tamanyo > self.Size1 and self.tamanyo < Size2:
                if dt > self.TimeToDel1:
                    archivos_a_borrar.append(na) # marca para borrar
            elif tamanyo > self.Size2:
                if  dt > self.TimeToDel2:
                    archivos_a_borrar.append(na) # marca para borrar
            
        # borrado
        for na in archivos_a_borrar:
            # log
            print '[REG] - Delete: File %(na)s size %(sz)d'\
                % {'na': na , 'sz': self.DictArchivos[na].Tam} , 'created at',\
                self.DictArchivos[na].FechaYHoraDeSubida , 'deleted!'

            try:
                os.remove(na) # borra archivo de disco
            except OSError:
                print '[REG] - Error: Trying to delete file %s' % na
                
            del(DictArchivos[na]) # borra del registro

            

    # comprueba las lista de archivos y si existen en el registro
    # crea nuevos registros si hay archivos nuevos.
    # Llama a la funcion ComprobarTiempoArchivos() para eliminar archivos
    # automaticamente segun `Parametros'
    def Actualizar(self):

        # lista los archivos y comprueba si estan en los registros
        try:
            nombres = os.listdir(self.Parametros.UploadFolder)
        except OSError:
            pass
        else:
            for nomb in nombres:
                nombre = os.path.join(self.Parametros.UploadFolder, nomb)
                #nombre = secure_filename(nombre)
                if self.ExisteNombre(nombre) == False:
                    # actualizar registro del nuevo archivo 
                    # este caso se deberia dar cuando se copia manualmente
                    # archivos en la carpeta UploadFolder.
                    
                    #self.DictArchivos[nombre] = DatosArchivo
                    dt_arch = DatosDeArchivo()
                    dt_arch.auto_init(nombre)
                    
                    self.DictArchivos[nombre] = dt_arch
                    
                    # nuevo reg
                    #self.getDictArchivos(nombre).auto_init(nombre)
                    #self.DictArchivos[nombre].auto_init(nombre)

                    # log TODO: activar este log solo si `LOG_REG' (implementar)
                    print '[REG] - New: File %(na)s size %(sz)d'\
                        % {'na': nombre , 'sz': self.DictArchivos[nombre].Tam},\
                        'created at', self.DictArchivos[nombre].FechaYHoraDeSubida
        # log
        print '[REG] - Updated!'
