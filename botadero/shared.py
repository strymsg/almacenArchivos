'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
# La idea de este archivo es almacenar objetos para que sean facilemente
# compartidos entre los distintos paquetes y modulos del proyecto.

from .configs import Parameters

# objetos globales y otros
globalParams = None
gr = {
    'storageUsed': 0,
    'storageTotal': 0,
    'filesNumber': 0
}
