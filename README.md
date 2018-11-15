* [Castellano](#es)
* [English](#en)
----
<h3 id="es">El Botadero</h3>

Servidor web centralizado para compartir archivos en una red local o internet.

Un directorio público donde cualquiera puede subir archivos y estos se pueden descargar libremente.

Para ahorrar espacio de almacenamiento, los archivos se borrar después de un número ajustable de días y también se evita la posiblidad de subir archivos duplicados usando algoritmos para obtener digestos sha1, md5, sha256, etc. 

Entre las funcionalidades que se pueden ajustar están:

* Intervalo de borrado.
* Almacenamiento máximo para archivos.
* Almacenamiento máximo por tamaño de archivo.
* Intervalo de borrado por tamaño de archivos.
* Nivel de verbosidad en archivos de reportes.
* Selección de algoritmo para digestos.
* Comprobación acelerada de digestos.
* Borrado de archivos usando passwords.
* Unidad de tiempo.

Esta aplicación no guarda datos sobre quién sube los archivos, licencia **AGPL**.

#### Instalación ####

Se utiliza python3 con el micro framework Flask, se puede instalar con los siguientes pasos:

pronto.

##### Para desarrollo #####

    # descargar el repositorio
    git clone https://notabug.org/strysg/botadero
	cd botadero
	# crear entorno virtual python 3
	virtualenv --python=python3 venv
	# activar entorno virtual
	. venv/bin/activate
	# instalar dependencias
	pip install -r rquirements.txt
	# variables de entorno
	export FLASK_APP=botadero.py
	export FLASK_ENV=development
	# ejecutar en modo desarrollo
	flask run

    # ejecutar pruebas
	pytest

#### Despliegue ####

pronto.

<h3 id="en">El Botadero</h3>

Centralized web server to share files on a local network or over the internet. 

A public directory where anyone can upload files and so they can be freely downlaoded.

To save storage, files are deleted after an adjustable number of days and file duplication is avoided by using sha1, md5, sha256, etc. digests.

Some customizable features are:

* File deletion interval.
* Maximun file storage size.
* Maximun file size for files.
* Deletion interval per file size.
* Verbosity level to log files.
* Digest algorithm selection.
* Accelerated digest.
* File deletion using password.
* Time unit.

This application does not store data about who upload files, **AGPL** License.

#### Install ####

It uses python3 and micro framework Flask, can be installed following:

soon.
	
##### For development #####

    # download project
    git clone https://notabug.org/strysg/botadero
	cd botadero
	# create python 3 virtual environment
	virtualenv --python=python3 venv
	# activate it
	. venv/bin/activate
	# install dependencies
	pip install -r rquirements.txt
	# environment variables
	export FLASK_APP=botadero.py
	export FLASK_ENV=development
	# run development mode
	flask run

    # testing
    pytest

#### Deploy ####

soon.

