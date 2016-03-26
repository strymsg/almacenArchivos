
## El Botadero ##

Una aplicación para compartir archivos públicamente.

La idea es compartir archivos, si alguien sube un archivo este se lista en la página principal y cualquiera puede descargarlo. Para ahorrar espacio de almacenamiento los archivos subidos se borran automáticamente después de X días dependiendo su tamaño.

Los parámetros como espacio de alamcenamiento reservado para la aplicación, tiempo para eliminación de archivos, máximo tamaño de archivos y otros, son configurables desde una archivo de configuracion.

*LICENCIA* **GPLv3**

*Requiere* [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

*Ejecucion* Una vez instalado python-flask: `python botadero.py`

Esta aplicación no usa bases de datos.

## Tareas por hacer

* Mejorar la apariencia.
* Hacer que los archivos se muestren por orden de subida.
* Probar el sistema de borrado automatico
* Implementar sistema detector de robots (captcha?).
* Implementar límites de subida por usuario, esto para prevenir que un usuario suba demasiados archivos.
* Acelerar la comprobacion de sha1sum al subir archivos.
* Guardar objeto EstadisticaArchivos en disco para recargarse rapidamente al inicio de la app.







