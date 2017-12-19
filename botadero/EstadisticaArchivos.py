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
import os

from botadero import ParametrosServidor
from botadero import DatosDeArchivo 

'''
Nota acerca de 'descincronizacion' cuando esta en produccion

Si no se usa self.CargarDesdeArchivo() , self.GuardarCambiosEnArchivo()
El objeto EstadisticaArchivos toma valores distintos a cada actualizacion
en el server web (por ejemplo NGINX) , como si el objeto estuviese siendo
compartido por varios procesos o hilos.

TODO: Averiguar como manejar un unico objeto en RAM comun a todos los hilos
      para no tener que cargarlo y guardarlo en disco duro como se hace
      actualmente.
'''
class EstadisticaArchivos:
    Parametros = ParametrosServidor.ParametrosServidor("parametros.txt", "")
    almacenDisponible = 0
    numArchivos = 0
    porcentajeAlmacenDisponible = 0
    PilaArchivos = []
    recalcular = False # ver como aprovechar este flag

    def __init__(self, NombreArchivoConfig, DebugLevel):
        self.Parametros = ParametrosServidor.\
                          ParametrosServidor(NombreArchivoConfig \
                                     , DebugLevel)
        self.almacenDisponible = 0
        self.porcentajealmacenDisponible = 0
        self.numArchivos = 0

        self.PilaArchivos = []

        self.Inicializar()

    def GetIndexArchivo(self, Nombre_con_ruta):
        i = 0
        for pa in self.PilaArchivos:
            if Nombre_con_ruta == os.path.join(self.Parametros.UploadFolder, \
                                               pa.categoria, pa.Nombre):
                return i
            i += 1
        return -1

    def GetDatosArchivo(self, Nombre):
        '''
        Devuelve el objeto datos_archivo correspondiente al Nombre de archivo dado
        NOTA: Se supone que ningun otro archivo tiene el mismo nombre.
        '''
        i = 0
        for pa in self.PilaArchivos:
            if Nombre == pa.Nombre:
                return self.PilaArchivos[i]
            i+=1
        return None
    
    def ExisteNombre(self, Nombre_con_ruta):
        '''
        Comprueba si el nombre de un archivo en la ruta dada ya existe 
        en los registros de archivos
        '''
        for da in self.PilaArchivos:
            if Nombre_con_ruta == os.path.join(self.Parametros.UploadFolder\
                                               ,da.categoria, da.Nombre):
                return True
        return False
        
    def ExisteNombreEstricto(self, Nombre):
        '''
        Comprueba si solamente el nombre del archivo ya existe en los
        registros de archivos
        '''
        for da in self.PilaArchivos:
            if Nombre == da.Nombre:
                return True
        return False

    def ExisteHash(self, Hash):
        ''' Comprueba si existe el hash en el registro de archivos'''
        print ("hash.... %s" % Hash)
        for da in self.PilaArchivos:
            print("nombre: %s  hash: %s" % [da.Nombre, da.HashCheck])
            if Hash == da.HashCheck:
                return True
        return False

    # TODO: analizar necesidad de esta funcion
    def ExisteArchivo(self, Nombre_con_ruta, hash_check):
        '''
        Comprueba si existe el archivo en la ruta dada existe.
        Ademas comprueba si la comprobacion hash corresponde a otro archivo,
        en los registros de archivos
        '''
        if self.ExisteNombre(Nombre_con_ruta):
            if self.GetDatosArchivo(Nombre_con_ruta).HashCheck == \
                hash_check:
                return True
            else:
                return False
        return False

    def ExisteArchivoEstricto(self, Nombre, hash_check):
        '''
        Comprueba si existe el nombre del archivo y si el hash_check
        corresponde a otro archivo en los registros de archivos.
        '''
        if self.ExisteNombreEstricto(Nombre):
            return True
        else:
            if self.ExisteHash(hash_check):
                return True
        return False

    def ExisteArchivoConTamanyo(self, tam):
        print ("-- tamanyo: %s" % tam)
        for da in self.PilaArchivos:
            #print(da.Tam)
            if tam == da.Tam:
                return True
        return False

    def ListaArchivosCategoria(self, categoria):
        '''
        Devuelve una lista con los nombres de los archivos 
        del registro de archivos que coincidan con la categoria dada
        '''
        lista_nombres = []
        for da in self.PilaArchivos:
            if da.categoria == categoria:
                lista_nombres.append(da.Nombre)
        #print "cat: %s |" %categoria , "la= %s" %lista_nombres
        return lista_nombres
        
    def IncrementarNumDescargas(self, Nombre_con_ruta):
        self.CargarDesdeDisco()
        i = self.GetIndexArchivo(Nombre_con_ruta)
        if i != -1:
            self.PilaArchivos[i].NumDescargas += 1
            print "[REG] - Download: Count increased to %d" \
                % self.PilaArchivos[i].NumDescargas,\
                "        of file %s" % Nombre_con_ruta
            self.GuardarCambiosEnDisco()
        else:
            print "[REG] - Error: File %s" % Nombre_con_ruta,\
                "        could not be found!"

    def AgregarArchivo(self, Nombre_con_ruta, hash_check, file):
        '''
        Agrega un nuevo archivo comprobando condiciones
        de tamanyo, espacio disponible, nombre, comprobacion hash.
        Si pasa estas pruebas el archivo se guarda en el disco
        y se crea un nuevo registro
        '''
        self.CargarDesdeDisco()
        # comprobacion de espacio disponible
        #TODO: Al parecer file.tell() no esta devolviendo el tamanyo exacto
        #      del archivo
        fsize = file.tell()
        
        file.seek(0)
        if (self.Parametros.TotalStorage - self.almacenDisponible) \
           + fsize > self.Parametros.TotalStorage:
            print "[STORAGE] - Error no free space: filesize %d" \
                % fsize, " only %d(ts) " % self.almacenDisponible, \
                " of space available."
            file.close()
            return 1
        # comprobacion de nombre
        elif self.ExisteNombre(Nombre_con_ruta):  # comprobacion de no duplicados
            print "[STORAGE] - Warning: File with name: %s "\
                % self.NombreSinRuta(Nombre_con_ruta), \
                "            exists, not uploaded."
            file.close()
            return 2
        # comprobacion de tamanyo
        #TODO: corregir esta comprobacion
        elif self.ExisteArchivoConTamanyo(fsize):
            # comprobacion de hash_check
            if self.ExisteArchivoEstricto(self.NombreSinRuta(Nombre_con_ruta), hash_check):
                print "[STORAGE] - Warning: hash check %s exists," % hash_check, \
                    "            not uploaded."
                file.close()
                return 3
        else:
            file.save(Nombre_con_ruta)  # save es un metodo propio de Flask
            file.close()
            # agrega el nuevo registro a las estadisticas
            da = DatosDeArchivo.DatosDeArchivo()
            da.auto_init(Nombre_con_ruta, \
                         self.Parametros.HashAlgorithm,\
                         self.Parametros.AccelerateHash,\
                         HashCheck=hash_check)
            self.PilaArchivos.append(da)
            self.GuardarCambiosEnDisco()
            self.ComprobarTiempoArchivos()

            print '[REG] - New File: %(na)s size %(sz)d'\
                % {'na': self.PilaArchivos[-1].categoria +'/'+ self.PilaArchivos[-1].Nombre ,\
                   'sz': self.PilaArchivos[-1].Tam},\
                '        created at', str(self.PilaArchivos[-1].FechaYHoraDeSubida)
            
            self.GuardarCambiosEnDisco()
            return 0
            
    def BorrarArchivo(self, Nombre):
        '''
        Borra un archivo dado el nombre, del disco y del registro de archivos.
        '''
        if self.ExisteNombreEstricto(Nombre):
            da = self.GetDatosArchivo(Nombre)
            cat = da.categoria
            pathf = os.path.abspath(self.Parametros.UploadFolder)
            # borra el archivo de disco
            try:
                os.remove(os.path.join(pathf, cat, Nombre))
            except:
                print "[DEL] File %s Not Found" %Nombre
            # borra el registro del archivo de la pila de registros
            del self.PilaArchivos[self.PilaArchivos.index(self.GetDatosArchivo(Nombre))]
            self.GuardarCambiosEnDisco()

    def Inicializar(self):
        '''
        Lee el objeto serializado en disco y si existe, copia sus configs
        en si mismo y retorna True.
        LLama tambien a la funcion ComprobrarTiempoArchivos()
        '''
        print "[REG] - Initializating..."
        self.Actualizar() # carga nuevos archivos si no estaban en el registro

    def Actualizar(self):
        '''
        Comprueba las lista de archivos viendo si existen en el registro,
        crea nuevos registros si hay archivos nuevos. Llama a
        ComprobarTiempoArchivos() 
        '''
        self.CargarDesdeDisco()
        ow = os.walk(self.Parametros.UploadFolder)
        '''
        NOTA: os.walk(top, topdown=True, onerror=None, followlinks=False)
        Generate the file names in a directory tree by walking the tree either top-down or bottom-up. For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple (dirpath, dirnames, filenames).'''
        p , directorios , archs = ow.next()
        '''NOTA: Solo se listan los archivos en una profundidad de directorios = 1 '''
        directorios += [p]
        for direc in directorios:

            if direc != self.Parametros.UploadFolder:
                direc = os.path.join(self.Parametros.UploadFolder, direc)
                
            nombres_con_rutas = self.ArchOrdenadosFechaSubida(direc)
            for nomb_con_ruta in nombres_con_rutas:
                if self.ExisteNombre(nomb_con_ruta) == False:
                    '''actualizar registro del nuevo archivo 
                    este caso se deberia dar cuando se copia manualmente
                    archivos en la carpeta `UploadFolder' '''
                    dt_arch = DatosDeArchivo.DatosDeArchivo()
                    dt_arch.auto_init(nomb_con_ruta, \
                                      self.Parametros.HashAlgorithm,\
                                      self.Parametros.AccelerateHash)
                    # agrega nuevo registro
                    self.PilaArchivos.append(dt_arch)
                    
                    print '[REG] - New: File %(na)s size %(sz)d'\
                        % {'na': self.PilaArchivos[-1].categoria+'/'+self.PilaArchivos[-1].Nombre, \
                           'sz': self.PilaArchivos[-1].Tam},\
                        'created at', self.PilaArchivos[-1].FechaYHoraDeSubida

                    self.GuardarCambiosEnDisco()
                else:
                    pass

            '''comprobacion si un archivo lo ha borrado un administrador
            esto se detecta cuando existe un archivo en el registro pero 
            no se encuentra en el directorio despues de listar archivos'''
            categoria = "" 
            if len(direc.split(os.path.sep)) > 1: # ej: almacen/Imagenes
                categoria = direc.split(os.path.sep)[-1]

            for nombre_arch in self.ListaArchivosCategoria(categoria):
                # se hace join por que `nombres_con_rutas' es del formato: 
                # almacen/categoria/nombre_arch | almacen/nombre_arch
                if os.path.join(self.Parametros.UploadFolder, categoria, nombre_arch)\
                   not in nombres_con_rutas:
                    print '[REG] - Delete: File %(ca)s/%(na)s , because it was manually deleted!'\
                        % {'ca':categoria , 'na': nombre_arch }
                    # borra el registro del archivo de la pila de registros
                    del self.PilaArchivos[self.PilaArchivos.index(self.GetDatosArchivo(nombre_arch))]

                    self.GuardarCambiosEnDisco()

        self.ComprobarTiempoArchivos()

        # determinacion de otros parametros estadisticos
        tam_total =0 
        for da in self.PilaArchivos:
            tam_total = tam_total + da.Tam
            
        self.almacenDisponible = self.Parametros.TotalStorage - tam_total
        self.porcentajealmacenDisponible = 100 - (tam_total * 100)\
                                           / self.almacenDisponible
        self.numArchivos = len(self.PilaArchivos)
        
        self.GuardarCambiosEnDisco()

        print '[REG] - Updated.' # log
        #self.MostrarRegistros() # muy verboson

    def ComprobarTiempoArchivo(self, Nombre):
        '''Comprueba si el registro del Nombre de archivo ha sobrepasado
        el tiempo permitido.
        Calcula los dias restantes del archivo.
        Retorna True si se ha sobrepasado y False si no.
        '''
        da = self.GetDatosArchivo(Nombre)
        edad = da.edad()
        vt = 0            
        tamanyo = da.Tam
        if tamanyo <  self.Parametros.Size1:
            vt = self.Parametros.TimeToDel0
        elif tamanyo >= self.Parametros.Size1 and \
             tamanyo <= self.Parametros.Size2:
            vt = self.Parametros.TimeToDel1 
        elif tamanyo > self.Parametros.Size2:
            vt = self.Parametros.TimeToDel2
        elif tamanyo >= self.Parametros.SizeMaxToUpload:
            vt = -1 # para borrar inmediatamente
        
        # marca si se ha excedido el tiempo
        if vt - edad < 0:
            return True
        else:
            da.DiasRestantes = vt - edad
            return False

    def ComprobarTiempoArchivos(self):
        '''Comprueba si uno o mas archivos han estado almacenados por mas
        dias de los especificados para su eliminacion.
        Los elimina automaticamente y los borra del registro, si no actualiza
        el registro de dias restantes'''
        self.CargarDesdeDisco()
        archivos_a_borrar = []
        for da in self.PilaArchivos:
            if self.ComprobarTiempoArchivo(da.Nombre):
                archivos_a_borrar.append(da.Nombre)
        # borrado
        for na in archivos_a_borrar:
            # log
            print '[REG] - Delete: File %(na)s size %(sz)d'\
                  % {'na': na , 'sz': self.GetDatosArchivo(na).Tam} , \
                  'created at: %s' %self.GetDatosArchivo(na).FechaYHoraDeSubida , \
                  'passed allowed time.'
            self.BorrarArchivo(na)
        self.GuardarCambiosEnDisco()

    def ArchOrdenadosFechaSubida(self, ruta):
        '''
        Devuelve la lista de los nonbres de archivos (con su ruta) 
        ordenados por fecha de subida (los mas nuevos al final)
        --> basdado en http://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python?lq=1
        '''
        try:
            ow = os.walk(ruta)
            p,d,files=ow.next()
        except OSError:
            print "[REG] - Error: Can't os.walk() on %s except OSError." %ruta
        else:
            nombs_rutas = [os.path.join(ruta, f) for f in files]
            nombs_rutas.sort(key=lambda x: os.path.getmtime(x))
        return nombs_rutas

        
    def GuardarCambiosEnDisco(self):
        '''
        Guarda todas las modificaciones hechas al registro en un archivo serializado 
        en disco duro.
        '''
        try:
            Eaf = open('EstadisticaArchivos.pkl', 'wb')
            pickle.dump(self ,Eaf)
            Eaf.close()
            print '[REG] - Saved to file EstadisticaArchivos.pkl'
            return True
        except:
            print '[REG] - Error: Object file EstadisticaArchivos.pkl could not be writen.'
            return False

    def CargarDesdeDisco(self):
        '''
        Carga el objeto con los datos guardados en el archivo serializado
        en disco duro.
        '''
        try:
            Eaf = open('EstadisticaArchivos.pkl', 'rb')
            Ea = pickle.load(Eaf)
            # copia el objeto guardado
            self.PilaArchivos = Ea.PilaArchivos
            self.almacenDisponible = Ea.almacenDisponible
            self.porcentajealmacenDisponible = Ea.porcentajealmacenDisponible
            self.numArchivos = self.numArchivos
            
            Eaf.close()
            print '[REG] - Loaded: Data from object file '\
                , '        EstadisticaArchivos.pkl'
            #self.Parametros.Reload_configs()
            return True
        except:
            print '[REG] - Warning: Not found object file '\
                , '        EstadisticaArchivos.pkl. Restarting, creating registers.'
            return False

    def MostrarRegistros(self):
        '''
        Mostrar todos los registros, para propositos de debug
        '''
        print '[REG] - ---------------------'
        print '[REG] - Showing all registers'
        print '[REG] - ---------------------'
        print 'Available: %s ' %self.almacenDisponible
        print 'Porcentaje Available: %s ' %self.porcentajeAlmacenDisponible
        print 'Show: Number of files: %s ' %self.numArchivos
        for pa in self.PilaArchivos:
            print 'File %(na)s size %(sz)d , hash_check %(hash)s'\
                % {'na': '#'+pa.categoria+' '+pa.Nombre, \
                   'sz': pa.Tam, 'hash': pa.HashCheck},\
                'created at', pa.FechaYHoraDeSubida
            print '---'
        
    def NombreSinRuta(self, Nombre_con_ruta):
        ''' Retorna el nombre del archivo sin la ruta
        '''
        return Nombre_con_ruta.split(os.path.sep)[-1]
