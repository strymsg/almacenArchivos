'''
This file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
from flask_sqlalchemy import SQLAlchemy
from .database import setup_db, db, get_db
from .models import Archivo
