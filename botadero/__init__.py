'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
import os
from flask import Flask

from .configs import Parameters
from .shared import globalParams

print ('__init.py<botadero>')

def create_app(config=None, instance_path=None, db_path=None):
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
    print ('\nINICIANDO\n')
    print ('os.environ.FLASK_ENV:', str(os.environ['FLASK_ENV']))
    print ('instance_path:', app.instance_path)

    # instance folders are not automatically created by flask
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # config file and parameters
    # if config is None:
        # nothing yet!
    if os.environ['FLASK_ENV'] == 'development':
        app.config.from_pyfile('../botadero/configs/configsDevelopment.py')
    elif os.environ['FLASK_ENV'] == 'production':
        app.config.from_pyfile('../botadero/configs/configs.py')
    print ('app.config:', str(app.config), '\n')

    # configuraciones adicionales
    globalParams = Parameters(app)
    print ('Parameters:',str(globalParams))

    # base de datos
    print ('Base de datos setup---')
    from . import database

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///db.sqlite3'
    with app.app_context():
        if db_path is None:
            database.setup_db(app)
        else:
            database.setup_db(app, db_path)

    # blueprints
    configure_blueprints(app)

    print ('\nCreating app finished!')
    return app
    
def configure_blueprints(app):
    from . import views
    app.register_blueprint(views.botaderoBp)
