# this file is part of "El Botadero"
# copyright Rodrigo Garcia 2018 <strysg@riseup.net>

import os
from flask import Flask

def create_app(config=None, instance_path=None):
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
    """
    app = Flask('botadero',
                instance_path=instance_path,
                instance_relative_config=True)
    print ('INICIANDO')
    print (app.instance_path)

    # instance folders are not automatically created by flask
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    
    # config file and parameters
    if config is None:
        app.config.from_pyfile('../botadero/configs/configsDevelopment.py')
    else:
        app.config.from_pyfile(config)

    # blueprints
    configure_blueprints(app)

    print ('app.config:', str(app.config), '\n')
    print ('Creating app finished')
    return app
    
def configure_app(app, config):
    pass

def configure_blueprints(app):
    from . import views
    app.register_blueprint(views.botaderoBp)

    














