## El Botadero ##

Una aplicación para compartir archivos públicamente.

La idea es compartir archivos, si alguien sube un archivo este se lista en la página principal y cualquiera puede descargarlo. Para ahorrar espacio de almacenamiento los archivos subidos se borran automáticamente después de X días dependiendo su tamaño.

Los parámetros como espacio de alamcenamiento reservado para la aplicación, tiempo para eliminación de archivos, máximo tamaño de archivos y otros, son configurables desde un archivo de configuracion [parametros.txt](parametros.txt).

La app optimiza el almacenamiento evitando que se suban archivos con el mismo nombre o mismo contenido.

*LICENCIA* **AGPL**

*Requiere* [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

*Ejecucion de pruebas*

Instalar virtualenv y python-pip,

`pip install paq1 paq2` , donde paq son la lista de paquetes en [pip_install.txt](Docu/pip_install.txt)

Después de activar el entorno virtual la app se ejecuta con:

`python2.7 botadero.py` y puede probarse en localhost:5000

*Despliegue en NGINX* ver [notas_deploy.txt](Docu/notas_deploy.txt)

*Revisar logs* tail -f logs/botadero.log

Esta aplicación no usa bases de datos.

## Tareas por hacer

Más urgentes primero.

* Hacer una apariencia "responsive".
* Implementar límites de subida por usuario, esto para prevenir que un usuario suba demasiados archivos.
* Acelerar la comprobacion sha1sum y subida de archivos.
* Hacer pruebas al despliegue del servicio documentado en [notas_deploy.txt](Docu/notas_deploy.txt)
* Implementar sistema detector de robots (captcha?).
* Revisar disclaimer en info/
