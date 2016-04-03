
## El Botadero ##

Una aplicación para compartir archivos públicamente.

La idea es compartir archivos, si alguien sube un archivo este se lista en la página principal y cualquiera puede descargarlo. Para ahorrar espacio de almacenamiento los archivos subidos se borran automáticamente después de X días dependiendo su tamaño.

Los parámetros como espacio de alamcenamiento reservado para la aplicación, tiempo para eliminación de archivos, máximo tamaño de archivos y otros, son configurables desde una archivo de configuracion.

La app optimiza el almacenamiento evitando que se suban archivos con el mismo nombre o mismo contenido.

*LICENCIA* **GPLv3**

*Requiere* [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

*Ejecucion* Una vez instalado python-flask: `python2.7 botadero.py`

Esta aplicación no usa bases de datos.

## Tareas por hacer

Más urgentes primero.

* Hacer una apariencia "responsive".
* Agregar contador de descargas.
* Implementar límites de subida por usuario, esto para prevenir que un usuario suba demasiados archivos.
* Agregar Disclaimer y revisar cambiar LICENCIA a AGPL.
* Desplegar el servicio y hacer pruebas iniciales.
* Acelerar la comprobacion sha1sum y subida de archivos.
* Implementar sistema detector de robots (captcha?).




