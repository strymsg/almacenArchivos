
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
import pickle
from botadero.Parametros_Servidor import *
from botadero.datos_archivo import *

class EstadisticaArchivos:
    def __init__(self, NombreArchivoConfig, DebugLevel):
        self.Parametros = ParametrosServidor(NombreArchivoConfig \
                                             , DebugLevel)
        self.AlmacenDisponible = 0
        self.PorcentajeAlmacenDisponible = 0
        self.NumArchivos = 0

        self.PilaArchivos = []
        self.PilaDiasRestantes = []

        self.Inicializar()

    def GetIndexArchivo(self, Nombre_con_ruta):
        i = 0
        for pa in self.PilaArchivos:
            if Nombre_con_ruta == pa.Nombre:
                return i
            i = i + 1
        return -1

    def GetDatosArchivo(self,  Nombre_con_ruta):
        i = 0
        for pa in self.PilaArchivos:
            if Nombre_con_ruta == pa.Nombre:
                return self.PilaArchivos[i]
            i = i + 1
                #return self.PilaArchivos.index(Nombre_con_ruta)
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

    def ExisteArchivoConTamanyo(self, tam):
        for da in self.PilaArchivos:
            if tam == da.Tam:
                return True
        return False
        
    def IncrementarNumDescargas(self, Nombre_con_ruta):
        self.CargarDesdeArchivo()
        i = self.GetIndexArchivo(Nombre_con_ruta)
        if i != -1:
            self.PilaArchivos[i].NumDescargas = self.PilaArchivos[i].NumDescargas + 1
            print "[REG] - Download: Count increased to %d" \
                % self.PilaArchivos[i].NumDescargas,\
                "        of file %s" % Nombre_con_ruta
            self.GuardarCambiosEnArchivo()
        else:
            print "[REG] - Error: File %s" % Nombre_con_ruta,\
                "        could not be found!"

    def AgregarArchivo(self, Nombre_con_ruta, sha1sum, file):
        
        # comprobacion de espacio disponible
        fsize = len(file.read())
        file.seek(0) # restarudando puntero
        if (self.Parametros.TotalStorage - self.AlmacenDisponible)\
           + fsize > self.Parametros.TotalStorage:
            print "[STORAGE] - Error no free space: filesize %d"\
                % fsize, " only %d(ts) " % self.AlmacenDisponible,\
                " of space available."
            file.close()
            return 1
        # comprobacion de nombre
        elif self.ExisteNombre(Nombre_con_ruta):
            print "[STORE] - Warn: File %s " % Nombre_con_ruta, \
                "            exists, not uploaded."
            file.close()
            return 2
        # comprobacion de tamanyo
        elif self.ExisteArchivoConTamanyo(fsize):
            # comprobacion de sha1sum
            if self.ExisteArchivo(Nombre_con_ruta, sha1sum):
                print "[STORE] - Warn: sha1sum %s exists," % sha1sum, \
                    "            not uploaded."
                file.close()
                return 3
        else:
            # guarda el archivo en disco
            file.save(Nombre_con_ruta)
            file.close()
            # agrega el nuevo registro a las estadisticas
            da = DatosDeArchivo()
            da.auto_init(Nombre_con_ruta)
            self.PilaArchivos.append(da)

            print '[REG] - New: File %(na)s size %(sz)d'\
                % {'na': self.PilaArchivos[-1].Nombre ,\
                   'sz': self.PilaArchivos[-1].Tam},\
                '        created at', self.PilaArchivos[-1].FechaYHoraDeSubida
            
            self.GuardarCambiosEnArchivo()
            return 0
            
    def BorrarArchivo(self, Nombre_con_ruta):
        if self.ExisteNombre(Nombre_con_ruta):
            # borra el archivo de disco
            os.remove(Nombre_con_ruta)
            # borra el registro del archivo del diccionario de registros
            del self.PilaArchivos[self.PilaArchivos.index(self.GetDatosArchivo(Nombre_con_ruta))]
            self.GuardarCambiosEnArchivo()

    # Lee objeto guardado en archivo y si existe, copia sus configs
    # en si mismo y retorna True.
    # Llama tambien a la funcion ComprobarTiempoArchivos()
    def Inicializar(self):
        self.CargarDesdeArchivo()
        self.Actualizar() # carga nuevos archivos si no estaban en el registro

    # comprueba las lista de archivos y si existen en el registro
    # crea nuevos registros si hay archivos nuevos. Llama a
    # ComprobarTiempoArchivos()
    def Actualizar(self):
        nombres = self.ArchOrdenadosFechaSubida(self.Parametros.UploadFolder)
        # comprueba si los archivos estan en los registros
        for nomb in nombres:
            #self.GetDatosArchivo(nomb) 
            if self.ExisteNombre(nomb) == False:
                # actualizar registro del nuevo archivo 
                # este caso se deberia dar cuando se copia manualmente
                # archivos en la carpeta `UploadFolder'
                dt_arch = DatosDeArchivo()
                dt_arch.auto_init(nomb)
                # agrega nuevo registro
                self.PilaArchivos.append(dt_arch)
                    
                print '[REG] - New: File %(na)s size %(sz)d'\
                    % {'na': nomb , 'sz': self.PilaArchivos[-1].Tam},\
                    'created at', self.PilaArchivos[-1].FechaYHoraDeSubida

                self.GuardarCambiosEnArchivo()

        self.ComprobarTiempoArchivos()

        # determinacion de otros parametros estadisticos
        tam_total =0 
        for da in self.PilaArchivos:
            tam_total = tam_total + da.Tam
            
        self.AlmacenDisponible = self.Parametros.TotalStorage - tam_total
        self.PorcentajeAlmacenDisponible = 100 - (tam_total * 100)\
                                           / self.AlmacenDisponible
        self.NumArchivos = len(self.PilaArchivos)
        
        print '[REG] - Updated.' # log

    

    # comprueba si uno o mas archivos han estado almacenados por mas
    # dias de los especificados para su eliminacion.
    # Los elimina automaticamente y los borra del registro
    def ComprobarTiempoArchivos(self):
        self.PilaDiasRestantes = [] # borra la lista para actualizarla
        archivos_a_borrar = []
        for da in self.PilaArchivos:
            edad = da.edad()
            vt = 0            
            # tamanyo
            tamanyo = da.Tam
            if tamanyo <  self.Parametros.Size1:
                vt = self.Parametros.TimeToDel0
            elif tamanyo >= self.Parametros.Size1 and \
               tamanyo <= self.Parametros.Size2:
                vt = self.Parametros.TimeToDel1 
            elif tamanyo > self.Parametros.Size2:
                vt = self.Parametros.TimeToDel2
            elif tamanyo >= self.Parametros.SizeMaxToUpload:
                vt = 999999 # para borrar inmediatamente
        
            # marca si se ha excedido el tiempo
            if vt - edad < 0:
                archivos_a_borrar.append(da.Nombre)
            else:
                self.PilaDiasRestantes.append(vt - edad)

        # borrado
        for na in archivos_a_borrar:
            # log
            print '[REG] - Delete: File %(na)s size %(sz)d'\
                  % {'na': na , 'sz': self.GetDatosArchivo(na).Tam} , \
                  'created at',self.GetDatosArchivo(na).FechaYHoraDeSubida , \
                  'surpassed allowed time.'
            self.BorrarArchivo(na)

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


    # Guarda todas las modificaciones hechas al registro en un archivo serializado en disco
    def GuardarCambiosEnArchivo(self):
        try:
            Eaf = open('EstadisticaArchivos.pkl', 'wb')
            pickle.dump(self ,Eaf)
            Eaf.close()
            print '[REG] - Saved to file EstadisticaArchivos.pkl'
            return True
        except:
            print '[REG] - Error: Object file EstadisticaArchivos.pkl could not be writen.'
            return False

    # Carga el objeto con los datos guardados en archivo serializado en disco
    def CargarDesdeArchivo(self):
        try:
            Eaf = open('EstadisticaArchivos.pkl', 'rb')
            Ea = pickle.load(Eaf)
            # copia el objeto guardado
            self.PilaArchivos = Ea.PilaArchivos
            self.AlmacenDisponible = Ea.AlmacenDisponible
            self.PorcentajeAlmacenDisponible = Ea.PorcentajeAlmacenDisponible
            self.NumArchivos = self.NumArchivos
            
            Eaf.close()
            print '[REG] - Loaded: Data from object file '\
                , '        EstadisticaArchivos.pkl'
            self.Parametros.Reload_configs()
            return True
        except:
            print '[REG] - Warning: Not found object file '\
                , '        EstadisticaArchivos.pkl. Restarting, creating registers.'
            self.Actualizar()
            return False
