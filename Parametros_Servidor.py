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
from logs import initLogs
import os

class ParametrosServidor:
    NombreArchivoConfig = ''
    TotalStorage = 0
    UploadFolder = ''
    Size1 = 0
    Size2 = 0
    TimeToDel0 = 0
    TimeToDel1 = 0
    TimeToDel2 = 0
    SizeMaxToUpload = 0
    LogFileName = ''
    DebugLevel = 0
        
    def __init__(self):
        self.NombreArchivoConfig = 'parametros.txt'
        self.TotalStorage = 0
        self.UploadFolder = "almacen"
        self.Size1 = 0
        self.Size2 = 0
        self.TimeToDel0 = 0
        self.TimeToDel1 = 0
        self.TimeToDel2 = 0
        self.SizeMaxToUpload = 0
        self.LogFileName = os.path.join('logs', 'botadero.log')
        self.DebugLevel = 0        

    def __init__(self, nombre_archivo_config, DebugLevel):
        self.init(nombre_archivo_config, DebugLevel)

    def init(self, nombre_archivo_config, DebugLevel):
        self.NombreArchivoConfig = nombre_archivo_config
        # configuraciones por defecto por si falla la carga desde archivo
        self.TotalStorage = 80000000000 #aprox 80 GB
        self.UploadFolder = "almacen"
        self.Size1 = 100000 # aprox 100 MB
        self.Size2 = 500000 # aprox 500 MB
        self.TimeToDel0 = 18 # 18 dias
        self.TimeToDel1 = 15 # 15 dias
        self.TimeToDel2 = 10 # 10 dias
        self.SizeMaxToUpload = 650000000000 # aprox 6.5 GB
        self.LogFileName = os.path.join('logs', 'botadero.log')
        self.DebugLevel = 20 # info

        # Inicializa el logueo
        initLogs(self.LogFileName , self.DebugLevel)
        
        err = self.Reload_configs()
        if err != 0:
            # registra el error
            print "[CONFIG_FILE] - Error loading file: %(nom)s - %(num)d wrong parameters" \
                %{'nom':self.NombreArchivoConfig, 'num':err}

    # Recargar las configuraciones desde el archivo de configuracion
    def Reload_configs(self):
        cont = ''
        err = 0
        # abriendo el archivo de configuraciones
        with open(self.NombreArchivoConfig, 'r') as f_parametros:
            for line in f_parametros:
                # detectar lineas validas con parametros
                lis = line.split(' ')
                if len(lis) > 1 and line[0] != '#' and line[0] != ' ' \
                   and line[0]!='\n':

                    if lis[0] == 'TOTAL_STORAGE':
                        if lis[1] != '' and int(lis[1] > 0):
                            self.TotalStorage = int(lis[1])
                        else:
                            err = err + 1
                            print '[CONFIG_FILE] - Error: TOTAL_STORAGE parameter'
                    elif lis[0] == 'SIZE_1' and int(lis[1] > 0):
                        if lis[1] != '' and int(lis[1] > 0):
                            self.Size1 = int(lis[1])
                        else:
                            err = err + 1
                            print '[CONFIG_FILE] - Error: SIZE_1 parameter'
                    elif lis[0] == 'SIZE_2':
                        if lis[1] != '' and int(lis[1] > 0):
                            self.Size2 = int(lis[1])
                        else:
                            err = err + 1
                            print '[CONFIG_FILE] - Error: SIZE_2 parameter'
                    if lis[0] == 'SIZE_MAX_TO_UPLOAD':
                        if lis[1] != '' and int(lis[1] > 0):
                            self.SizeMaxToUpload = int(lis[1])
                        else:
                            err = err + 1
                            print '[CONFIG_FILE] - Error: TOTAL_STORAGE parameter'
                    elif lis[0] == 'TIME_TO_DEL_0':
                        if lis[1] != '' and int(lis[1] > 0):
                            self.TimeToDel1 = int(lis[1])
                        else:
                            err = err + 1
                            print '[CONFIG_FILE] - Error: TIME_TO_DEL_0 parameter'
                    elif lis[0] == 'TIME_TO_DEL_1':
                        if lis[1] != '' and int(lis[1] > 0):
                            self.TimeToDel1 = int(lis[1])
                        else:
                            err = err + 1
                            print '[CONFIG_FILE] - Error: TIME_TO_DEL_1 parameter'
                    elif lis[0] == 'TIME_TO_DEL_2':
                        if lis[1] != '' and int(lis[1] > 0):
                            self.TimeToDel2 = int(lis[1])
                        else:
                            err = err + 1
                            print '[CONFIG_FILE] - Error: TIME_TO_DEL_2 parameter'
        return err
