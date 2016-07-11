'''
This file is part of Botadero
'''
import os, sys, datetime, hashlib

class DatosDeArchivo:
    Nombre = ''
    Tam = 0
    FechaYHoraDeSubida = datetime.datetime.now()
    Extension = ''
    NumDescargas = 0
    sha1sum = ''
    categoria = ''
    DiasRestantes = 100

    def __init__(self):
        self.Nombre = ''
        self.Tam = 0
        self.FechaYHoraDeSubida = datetime.datetime.now()
        self.Extension = ''
        self.NumDescargas = 0
        self.sha1sum = ''
        self.categoria = ''
        self.DiasRestantes = 100

    def auto_init(self, Nombre_con_ruta, sha1sum=None):
        ''' Se guarda el nombre del archivo y su categoria si tiene:
        ej: almacen/entrevista.ogg
            Nombre=entrevista.ogg
            categoria=''
        ej: almacen/videos/inaguracion1_2015.ogv
            Nombre=inaguracion1_2015.ogv
            categoria=videos
        '''
        ## determinacion de atributos
        #self.Nombre = Nombre_con_ruta
        self.Nombre = nombre_archivo(Nombre_con_ruta)
        self.categoria = categoria_archivo(Nombre_con_ruta)
        # tamanyo
        self.Tam = os.stat(Nombre_con_ruta).st_size
        # Extension
        self.Extension = ''
        if len(Nombre_con_ruta.rsplit('.', 1)) > 1:
            self.Extension = Nombre_con_ruta.rsplit('.', 1 )[1]
        # NumDescargas
        self.NumDescargas = 0
        # sha1sum
        if sha1sum is None:
            with open(Nombre_con_ruta, 'r') as fil:
                self.sha1sum = self.arch_sha1sum(fil)
        else:
            self.sha1sum = sha1sum
        # Fecha y hora simula creacion del archivo ahora.
        self.FechaYHoraDeSubida = datetime.datetime.now()
        # DiasRestantes
        self.DiasRestantes = 100 # dummy

    def arch_sha1sum(self, archivo):
        '''Recibe un objeto archivo y devulve el sha1sum
        Nota: No se restaura el puntero ni se cierra el archivo.'''
        archivo.seek(0) # puntero en 0
        t_ant = -1
        t_act = archivo.tell()
        pedazo_tam = 125*1024
        h = hashlib.sha1()
        # obtiene el sha1sum del archivo por pedazos de 125 MB a lo maximo
        # esto lo hace en caso de ser un archivo con tamanyo mas grande que 2GB
        # por ser su contenido mayor que el maximo de una cadena (2^32)
        print "[REG] - Getting sha1sum, wait please ..."
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
        #return (datetime.datetime.now() - self.FechaYHoraDeSubida).days
        return (datetime.datetime.now() - self.FechaYHoraDeSubida).seconds

def nombre_archivo(Nombre_con_ruta=None):
    tupla = Nombre_con_ruta.split(os.sep)
    return tupla[-1]

def categoria_archivo(Nombre_con_ruta=None):
    tupla = Nombre_con_ruta.split(os.sep)
    if len(tupla)>2:
        return tupla[-2]
    return ''    

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

    
        
        
