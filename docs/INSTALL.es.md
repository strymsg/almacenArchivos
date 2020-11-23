# Instalación de aplicación el almacén de archivos

Este manual asume que se está trabajando sobre una distribución de GNU/Linux derivada de Debian.

Primero es necesario instalar las dependencias de la aplicación, se necesita que este instalado en el sistema `python3 python3-dev pip3 virtualenv`.

```bash
git clone https://notabug.org/strysg/botadero/

cd botadero # o nombre del proyecto
# instalando entorno virtual python
virtualenv --python=python3 venv

# activar el entorno virtual
. venv/bin/activate

# instalar dependencias
pip install -r requirements.txt
```
## Modo Desarrollo

### Archivo de configuración

Las configuraciones se hacen renombrando el archivo `botadero/configs/configsDevelopment.py.sample` como `botadero/configs/configsDevelopment.py` y luego ajustando los valores según conveniencia.

### Iniciar la aplicación (modo desarrollo)

```bash
export FLASK_ENV=development
export FLASK_APP=botadero.py
flask run
```

Que debería iniciar la aplicación accesible desde http://localhost:5000 en modo desarrollo y leerá el archivo `botadero/configs/configsDevelopment.py`.

### Notas sobre subida de archivos y modo desarrollo

Por [limitaciones del servidor de desarrollo](https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#improving-uploads) cuando se suben archivos grandes se generan errores *connection reset*, esto se corrige al usar `uwsgi` en entorno de producción.

### Sobre actualización de lista de archivos

La aplicación **necesita** que se ejecute el script `cronjobs.py` que se encarga de controlar el tiempo de borrado de los archivos, cuando estos exceden su tiempo permitido los elimina y actualiza las páginas de templates jinja2.

Se puede ejecutar manualmente con:

```bash
venv/bin/python cronjobs.py
```

O agregando una tarea programada, si no se ejecuta este script periódicamente, **no se actulizará** el tiempo de borrado de archivos a menos que se suban o eliminen archivos desde la interfaz web. 

La aplicación **no renderiza** los templates de las páginas de archivos cada que se ingresa a una ruta de listado de archivos. La acción de renderización (usando el motor de templates jinja2) se hace en luego de que se dan cualquiera de los siguientes acciones:

- Se ejecuta `cronjobs.py`.
- Se sube un archivo (mediante la interfaz web).
- Se elimina un archivo (mediante la interfaz web).

Una forma de forzar la actualización de las páginas siendo mostradas es poner a 1 el campo `renderHtml` de las páginas en la tabla `html_page` de la base de datos `botadero/db.sqlite` que usa la aplicación.

### Sobre categorías (carpetas dentro de la carpeta almacén)

La aplicación guarda los archivos compartidos por defecto en `almacen/` y permite la creación de subcarpetas (de profundidad uno) dentro, por ejemplo `almacen/documentos`, `almacen/imágenes`, etc. Las categorías se detectan al ejecutar `cronjobs.py`.

## Modo producción

### Iniciar la aplicación (ambiente de producción)

Para este caso se debería usar `uwsgi` y un servidor web como `nginx` y el archivo `botadero/configs/configs.py`.

### Ejecutar uwsgi

Se hace usando el archivo `app.ini` y si es necesario hay que ajsutarlo. Se ejecuta por ejemplo dentro de la carpeta del proyecto.

```bash
# Asumiendo que se tiene el entorno virtual inicializado
export FLASK_ENV=production
export FLASK_APP=botadero

uwsgi --ini app.ini

# Si no se tiene iniciado el entorno virtual python funciona también
venv/bin/uwsgi --ini app.ini
```
En la consola debería aparecer que la aplicación se ha iniciado.

### Nginx

Se usará nginx como servidor de proxy reverso wsgi, este un ejemplo de las configuraciones suponiendo que creamos un nuevo archivo `/etc/nginx/conf.d/almacen.conf`:

```
server {
       server_name ip_o_dominio;

       # permite la subida de archivos de hasta 5000 MB
       client_max_body_size 5000M;

       location / {
             include uwsgi_params;
			 # socket unix, el mismo que indica el archivo app.ini
             uwsgi_pass unix:/tmp/almacen_archivos.sock;
			 
             # Para que nginx sea tolerante con conexiones lentas (opcional)
             uwsgi_read_timeout 300s;
             uwsgi_send_timeout 300s;
       }

       location /robots.txt {
         alias /ruta/aplicacion/almacenArchivos/botadero/static/robots.txt;
       }
}
```
Luego se reinicia nginx y este quedará en modo escucha.

Puede que se tengan problemas con permisos cuando nginx no pueda leer el socket y resulte en el error `unix:/tmp/almacen_archivos.sock failed (13: Permission denied)` asi que habrá que asegurarse que el usuario de nginx pueda acceder al socket que indica el archivo `app.ini` (por defecto /tmp/almacen_archivos.sock).

Una opción es agregar el usuario que ejecuta la aplicación al grupo www-data por ejemplo con:

```
gpasswd -a usuario www-data
# o más drástico pero quizá no recomendado agregar a www-data al grupo del usuario
gpasswd -a www-data usuario
```

### Actualización y borrado de archivos

Como se menciona arriba la aplicación **necesita** que se ejecute el script `cronjobs.py`. En producción es conveniente agregar una tarea programada por ejemplo para sistemas UNIX en /etc/crontab.

```
*/2 *   * * *   www-data    cd /srv/almacen_archivos; export FLASK_ENV=production;venv/bin/python3 cronjobs.py >> cronjobs.log 2>&1
```
Que ejecuta como usuario `www-data` cada 2 minutos el script `cronjobs.py` y guarda el resultado (incluyendo errores) en un archivo cronjobs.log.

### Ejemplo despliegue con supervisorctl

Si se usa supervisor un archivo de ejemplo sería este asumiendo que el proyecto esta instalado en `/srv/almacen_archivos` y aprovechamos el archivo `run.sh`:

```
[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)

[supervisord]
logfile=/tmp/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=50MB       ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=5          ; (num of main logfile rotation backups;default 10)
loglevel=info               ; (log level;default info; others: debug,warn,trace)
pidfile=/tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
nodaemon=false              ; (start in foreground if true;default false)
minfds=1024                 ; (min. avail startup file descriptors;default 1024)
minprocs=200                ; (min. avail process descriptors;default 200)

[supervisorctl]
serverurl=unix:///srv/botadero/almacen_archivos.sock

[program:almacen_archivos]
command=/bin/sh /srv/almacen_archivos/run.sh
directory=/srv/almacen_archivos/
user=www-data
autostart=true
autorestart=true
stdout_logfile=/srv/alamcen_archivos/uwsgi.log ; log file
redirect_stderr=true
stopsignal=QUIT
```

Luego se recarga la configuracion y reinicia el servicio con supervisor:

```bash
$ sudo supervisorctl reread
$ sudo supervisorctl restart almacen_archivos
```
