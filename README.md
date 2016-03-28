
## El Botadero ##

Una aplicación para compartir archivos públicamente.

La idea es compartir archivos, si alguien sube un archivo este se lista en la página principal y cualquiera puede descargarlo. Para ahorrar espacio de almacenamiento los archivos subidos se borran automáticamente después de X días dependiendo su tamaño.

Los parámetros como espacio de alamcenamiento reservado para la aplicación, tiempo para eliminación de archivos, máximo tamaño de archivos y otros, son configurables desde una archivo de configuracion.

La app optimiza el almacenamiento evitando que se suban archivos con el mismo nombre o mismo contenido.

*LICENCIA* **GPLv3**

*Requiere* [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

*Ejecucion* Una vez instalado python-flask: `python botadero.py`

Esta aplicación no usa bases de datos.

## Tareas por hacer

* Probar el sistema de borrado automatico.
* Acelerar la comprobacion sha1sum al subir archivos.
* Implementar sistema detector de robots (captcha?).
* Implementar límites de subida por usuario, esto para prevenir que un usuario suba demasiados archivos.






