from flask import request, redirect, url_for
from logs import initLogs

class ParametrosServidor:
    def __init__(nombre_archivo_config, DebugLevel):
        self.NombreArchivoConfig = nombre_archivo_config
        # Defaults if reload config fails
        self.TotalStorage = 80 000 000 #aprox 80 GB
        self.UploadFolder = "almacen/"
        self.Size1 = 100000 # aprox 100 MB
        self.Size2 = 500000 # aprox 500 MB
        self.TimeToDel1 = 15 # 15 days
        self.TimeToDel2 = 10 # 10 days
        self.SizeMaxToUpload = 6 500 000 # aprox 6.5 GB
        self.LogFileName = 'botadero.log'
        self.DebugLevel = 20 # info
        # initializes loggin
        initLogs(LogFileName , self.DebugLevel)
        
        if Reload_configs() != 0:
            # log an error
            print "[CONFIG_FILE] - Error loading file: %" \
                %self.NombreArchivoConfig

    def Reload_configs():
        cont = ''
        with open(self.NombreArchivoConfig, 'r') as f_parametros:
            for line in f_parametros:
                # detectar lineas validas con parametros
                if line[0] != '#' and line[0] != ' ' and line[0]!='\n':
                    param = line[0]
                    if param == 'TOTAL_STORAGE':
                        TOTAL_STORAGE = int(param)
                    elif param == 'UPLOAD_FOLDER':
                        UPLOAD_FOLDER = param
                    elif param == 'SIZE_1':
                        SIZE_1 = int(param)
                    elif param == 'SIZE_2':
                        SIZE_2 = int(param)
                    elif param == 'TIME_TO_DEL_1':
                        TIME_TO_DEL_1 = int(param)
                    elif param == 'TIME_TO_DEL_2':
                        TIME_TO_DEL_2 = int(param)
                        #cont = cont + '>>'
                        #cont = cont + line + '<br>'
                        return ''
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #test
    #res = str(TOTAL_STORAGE), UPLOAD_FOLDER, str(SIZE_1), str(SIZE_2), str(TIME_TO_DEL_1), str(TIME_TO_DEL_2)
    #return res

# # Leer el archivo `parametros.txt' y guardar configuraciones en RAM
# def Reload_parameters():
#     cont = ''
#     with open('parametros.txt', 'r') as f_parametros:
#         for line in f_parametros:
#             # detectar lineas validas con parametros
#             if line[0] != '#' and line[0] != ' ' and line[0]!='\n':
#                 param = line[0]
#                 if param == 'TOTAL_STORAGE':
#                     TOTAL_STORAGE = int(param)
#                 elif param == 'UPLOAD_FOLDER':
#                     UPLOAD_FOLDER = param
#                 elif param == 'SIZE_1':
#                     SIZE_1 = int(param)
#                 elif param == 'SIZE_2':
#                     SIZE_2 = int(param)
#                 elif param == 'TIME_TO_DEL_1':
#                     TIME_TO_DEL_1 = int(param)
#                 elif param == 'TIME_TO_DEL_2':
#                     TIME_TO_DEL_2 = int(param)
#                 #cont = cont + '>>'
#             #cont = cont + line + '<br>'

#     #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#     #test
#     #res = str(TOTAL_STORAGE), UPLOAD_FOLDER, str(SIZE_1), str(SIZE_2), str(TIME_TO_DEL_1), str(TIME_TO_DEL_2)
#     #return res
#     return ''

        
