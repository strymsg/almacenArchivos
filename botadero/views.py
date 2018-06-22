import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask import current_app as app

botaderoBp = Blueprint('botadero', __name__, url_prefix='')

# prueba primera vista
@botaderoBp.route('/')
def hi():
    print ('Hola botadero')
    return ('initial point')

