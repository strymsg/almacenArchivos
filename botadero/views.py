import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

botaderoBp = Blueprint('botadero', __name__, url_prefix='')

# prueba primera vista
@botaderoBp.route('/')
def hi():
    print ('Hola botadero')
    return "Hola botadero"

