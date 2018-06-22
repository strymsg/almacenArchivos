###### Archivo de configuración del Botadero ######

# Tamaño máximo en bytes que se puede almacenar
# (para este ejemplo se usa 10.5 GB)
TOTAL_STORAGE = 10500000000

# Directorio se almacenan los archivos compartidos
UPLOAD_DIRECTORY = "almacen"

# Objeto que define Tamaño de archivos a considerar (en Bytes) y en cuantas unidades de tiempo borrarlos.
# En este este ejemplo se definen cuatro tamaños a considerar (9MB, 20MB, 40MB y 220 MB
SIZE_LIMITS_AND_TIME_TO_DELETE = [
    [{'9000000': 16}],
    [{'20000000': 11}],
    [{'40000000': 8}],
    [{'220000000': 6}]
]

# Nivel de verbosidad para guardar registros de eventos
# 0 = ERROR
# 1 = INFO
# 2 = DEBUG
LOG_LEVEL = 1

# True fuerza la comprobación, False cancela la comprobación al subir archivos
DIGEST_CHECK = True

# El algoritmo para hacer la comprobación hash, se puede usar 'md5', 'sha1', 'sha224', 'sha384', 'sha256', 'sha512'
DIGEST_ALGORITHM = 'sha1'

# Acelera la comprobación hash leyendo sólo porciones de cada archivo.
DIGEST_ACCELERATED = False

# Si se puede usar passwords al subir archivos.
# cuando se usa password, se puede marcar el archivo para borrarlo siempre y cuando se introduzca el mismo password que se usó para subirlo.
PASSWORD_USE = False

# Usar un reto captcha al subir archivos
CAPTCHA_USE = False

######### Opciones de configuración de FLASK ##########

# cuando se pone la app en produccion Usar DEBUG = False
DEBUG = False
SECRET_KEY = 'Llave secreta tiene que ir aqui'
