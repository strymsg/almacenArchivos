## El Botadero ##

Una aplicación para compartir archivos públicamente.

La idea es compartir archivos, si alguien sube un archivo este se lista en la página principal y cualquiera puede descargarlo. Para ahorrar espacio de almacenamiento los archivos subidos se borran automáticamente después de X días dependiendo su tamaño.

Los parámetros como espacio de alamcenamiento reservado para la aplicación, tiempo para eliminación de archivos, máximo tamaño de archivos y otros, son configurables desde un archivo de configuracion [parametros.txt](parametros.txt).

La app optimiza el almacenamiento evitando que se suban archivos con el mismo nombre o contenido.
El botadero soporta categorías (que son directorios dentro la carpeta almacen/) ver [Docu/categorias.txt](Docu/categorias.txt)

*LICENCIA* **AGPL**

*Requiere* [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

**Ejecucion de pruebas**

Instalar virtualenv y python-pip, activar el entorno virtual, luego:

`pip install paq1 paq2` , donde paq son la lista de paquetes en [pip_install.txt](Docu/pip_install.txt), en general basta con:

`pip install Flask`
`pip install uwsgi`

Se debe activar el entorno virtual: `. venv/bin/activate`, luego para ejectuar la app:

`python2.7 runserver.py` y puede probarse en `localhost:5000`

*Despliegue en NGINX (Actualizar)* ver [deploy_debian](Docu/notas_deploy_nginx_debian.txt), [deploy_ubuntu](Docu/notas_deploy_nginx_ubuntu.txt)

*Revisar logs* `tail -f logs/botadero.log`

Esta aplicación no usa bases de datos.

## Tareas por hacer

Más urgentes primero.

* Hacer una apariencia "responsive".
* Agregar barra de progreso al subir archivos.
* Acelerar la comprobacion sha1sum y subida de archivos.
* Implementar límites de subida por usuario, esto para prevenir que un usuario suba demasiados archivos.
* Implementar sistema detector de robots (captcha?).
* Revisar disclaimer en info/
