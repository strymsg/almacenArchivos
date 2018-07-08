import os
from botadero import create_app
from botadero import database

from flask_alembic import Alembic

app = create_app()

alembic = Alembic()
alembic.init_app(app)

if __name__ == 'main':
    manager.run()
