'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
import os
from flask import Flask, g
from logging.config import dictConfig

from .configs import Parameters
######
# Nota importante si solo se usa 'from .shared import globalParams' dentro
# de este modulo *se crea una copia* local de `globalParams' de shared
# y las modificaciones aqui no suponen un cambio global
# por eso se utiliza from . import shared
######
from . import shared

def create_app(config=None, instance_path=None, db_path='sqlite:///db.sqlite3', testing=False):
    """ Crear la app.
    :param instance_path: An alternative instance path for the application.
                          By default the folder ``'instance'`` next to the
                          package or module is assumed to be the instance
                          path.
                          See :ref:`Instance Folders <flask:instance-folders>`.
    :param config: The configuration file or object.
                   The environment variable is weightet as the heaviest.
                   For example, if the config is specified via an file
                   and a ENVVAR, it will load the config via the file and
                   later overwrite it from the ENVVAR.

    :param db_path: Database URI to be `SQLALCHEMY_DATABASE_URI', if not 
    provided it uses 'sqlite:///db.sqlite3'
    """
    app = Flask(__name__,
                instance_path=instance_path,
                instance_relative_config=True)

    print('\nINICIANDO\n')
    print('os.environ.FLASK_ENV:', str(os.environ['FLASK_ENV']))
    print('instance_path:', app.instance_path)

    # instance folders are not automatically created by flask
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Aditional parameters
    # if config is None:
        # nothing yet!
    if os.environ['FLASK_ENV'] == 'development':
        app.config.from_pyfile('../botadero/configs/configsDevelopment.py')
    elif os.environ['FLASK_ENV'] == 'production':
        app.config.from_pyfile('../botadero/configs/configs.py')

    ctx = app.app_context()
    ctx.push()
    
    init_logs(app, app.config)
        
    g.log.warning('app.config:\n {0}\n'.format(str(app.config)))

    # configuraciones adicionales
    shared.globalParams = Parameters(app)
    g.log.warning('--Configs cargadas--\n {0}'.format(str(shared.globalParams)))

    app.config['UPLOAD_FOLDER'] = shared.globalParams.uploadDirectory
    # Se agrega 50% por que al parecer cuando se envian archivos de gran tamaño
    # Crecen las peticiones y el tamaño real de la petición excede a de los archivos
    app.config['MAX_CONTENT_LENGTH'] = int(shared.globalParams.sizeLimitsAndTimeToDelete[0][0]*1.5)

    g.log.warning('Max file size (config file): {0}'
                  .format(
                      shared.globalParams.sizeLimitsAndTimeToDelete[0][0]))
    g.log.warning('Max file app.config: {0}'
                  .format(app.config['MAX_CONTENT_LENGTH']))
    
    # base de datos
    g.log.warning('\nBase de datos setup---')
    from . import database

    # ctx = app.app_context()
    # ctx.push()
    database.setup_db(app, db_path=db_path, testing=testing)
    
    # blueprints
    configure_blueprints(app)

    g.log.warning('\n   Creating app finished!')
    return app

def init_logs(app, config):
    # armando diccionario de logs
    logsConfig = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'root': {
            'level': config['LOG_LEVEL'],
            'handlers': ['wsgi']
        }
    }
    if config['LOG_TODISK'] is True:
        logsConfig['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'filename': config['LOG_FILENAME'],
            'formatter': 'default',
            'level': config['LOG_LEVEL']
        }
        logsConfig['root']['handlers'].append('file')
    if os.environ['FLASK_ENV'] == 'development':
        logsConfig['handlers']['console'] = {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout'
        }
        logsConfig['root']['handlers'].append('console')
    # cargando logs
    dictConfig(logsConfig)
    g.log = app.logger

def configure_blueprints(app):
    from . import views
    app.register_blueprint(views.botaderoBp)
