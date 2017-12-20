## El Botadero ##

Una aplicación para compartir archivos públicamente.

La idea es compartir archivos, si alguien sube un archivo, este se lista en la página principal y cualquiera puede descargarlo. Para ahorrar espacio de almacenamiento los archivos subidos se borran automáticamente después de X días dependiendo su tamaño.

Los parámetros como espacio de alamcenamiento reservado para la aplicación, tiempo para eliminación de archivos, máximo tamaño de archivos y otros, son configurables desde un archivo de configuracion [parametros.txt](parametros.txt).

La app optimiza el almacenamiento evitando que se suban archivos con el mismo nombre o contenido.
El botadero soporta categorías (que son directorios dentro la carpeta almacen/) ver [Docu/categorias.txt](Docu/categorias.txt)

*LICENCIA* **AGPL**

*Requiere* [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

**Ejecucion de pruebas**

* `mkdir botadero_pruebas; cd botadero_pruebas`
* `git clone https://notabug.org/strysg/botadero` o descomprimir si se ha descargado en .zip 
* Instalar `virtualenv` , `python-pip` , crear un entorno virtual python2.7, luego:
* Activar el entorno virtual de la carpeta actual: `. venv/bin/activate`
* `pip install Flask`
* `pip install uwsgi`

Ejecutar la app con:

`python2.7 runserver.py` y puede probarse en `localhost:5000`

*Revisar logs* `tail -f logs/botadero.log`

## Despliegue con NGINX ##

* [debian](Docu/notas_deploy_nginx_debian.txt)
* [ubuntu](Docu/notas_deploy_nginx_ubuntu.txt)

*NOTA:* ajustar `application.debug` del archivo [runserver.py](runserver.py) adecuadamente para desarrollo o produccion.

*Revisar logs* `tail -f logs/botadero.log`

Esta aplicación no usa bases de datos.

## Tareas por hacer ##

Más urgentes primero.

* [BUG] Arreglar el problema cuando se suben archivos estos se copian en al parecer un buffer, luego una vez se comprueba no duplicacion se copia el archivo nuevamente al directorio, analizar si es necesario moverlo o establecer el directorio destino como "buffer". (Para profundizar eso, se debe estudiar flask (metodo save() en flask_uploads.py) y werkzeug (datastructures.py) para dominar la forma en que se guardan los archivos subidos.
* [IMPROVE] Comprobar si el nombre del archivo que se quiere subir ya existe (antes de hacer el hash o siquiera empezar a recibir el archivo)
* Arreglar soporte para descargar archivos mas grandes que 2GB en servidor web (parece una configuracion propia de cada servidor web como NGINX o Apache2).
* [IMPROVE] Individualizar barra de progreso al subir archivos.
* [IMPRIVE] Agregar posiblidad de borrar archivos haciendo que se puede especificar password al subir el archivo.
* Implementar límites de subida por visitante, esto para prevenir que un@ visitante suba demasiados archivos.
* Implementar sistema detector de robots (captcha?).
* Revisar disclaimer en info/
