''' 
El Botadero, una aplicación web para compartir archivos libremente.
Copyright (C) 2018 Rodrigo Garcia <strysg@riseup.net>
'''
from flask_sqlalchemy import SQLAlchemy
from .database import init_db
from .models import Archivo
