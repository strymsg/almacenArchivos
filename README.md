* [English description](#english)

## El Botadero ##

Una aplicación para compartir archivos públicamente.

La idea es compartir archivos, si alguien sube un archivo este se lista en la página principal y cualquiera puede descargarlo. Para ahorrar espacio de almacenamiento los archivos subidos se borran automáticamente después de X días dependiendo su tamaño.

Los parámetros como espacio de alamcenamiento reservado la aplicación, tiempo para eliminación de archivos, máximo tamaño de archivos y otros, son configurables.

`LICENCIA` **GPLv3**

`Requiere` [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

Esta aplicación no usa bases de datos.

## Tareas por hacer

* Cargar parámetros a partir de archivo de configuración.
* Implementar el borrado automático de archivos siguiendo parámetros cargados.
* Mejorar la apariencia.
* Implementar sistema detector de robots (captcha?).
* Implementar límites de subida por usuario, esto para prevenir que un usuario suba demasiados archivos.

<h4 id="english"> </h4>

## El botadero ##

An aplication to share files.

The main idea is to share files, if somebody uploads a file, the file is shown on the main page and anyone can download it. To save physical storage the uploaded files will be deleted after X days depending on their size.

Parameters like physical storage for the app, time to delete files, maximun file size and others, can be set using configuration files.

`LICENCE` **GPLv3**

`Requires` [Python-flask](http://flask.pocoo.org/docs/0.10/installation/#installation)

This app does not use a database.

## TODO

* Load parameters from configuration files.
* Implement auto deletion of files following loaded parameters.
* Improve appareance.
* Implement a robot detector system (captcha?)
* Implement a limitations for single users, to prevent a single user to upload too much files.








