#!/bin/bash

# script para actualizar el botadero deployado
# a la ultima version de desarrollo.
# Se asume que se ha desplegado el servicio antes.

# Para esto es necesario reemplazar los archivos .py,
# y posiblemente parametros.txt
# e ingorar los directorios almacen/ logs/ venv/
# y posiblemente EstadisticasArchivos.pkl

# luego asignar los permisos al usuario www-data

DIR_BOTADERO_PRODUCCION=$1
DIR_BOTADERO_DESARROLLO=$2

#

