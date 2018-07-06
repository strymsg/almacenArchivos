# this file is part of "El Botadero"
# copyright Rodrigo Garcia 2018 <strysg@riseup.net>
# AGPL liberated.

import functools

from . import controller
from . import utils as u

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

botaderoBp = Blueprint('botadero', __name__, url_prefix='')

# prueba primera vista
@botaderoBp.route('/')
def indexView():
    print ('Hola botadero')

    dv = {
        'esquemaColores':u.esquemaColoresRandom(),
        'categoriaActual': 'Misc',
        'categorias': {
            'categoria1': [
                {'name': 'arch1.jpeg', 'size': 88418, 'date': '2018-06-14 19:49:17.427922', 'restante': 2},
                {'name': 'arch2.jpeg', 'size': 128418, 'date': '2018-06-22 19:49:17.427922', 'restante': 11},
                {'name': 'juef.zip', 'size': 9928418, 'date': '2018-06-20 19:49:17.427922', 'restante': 8},
                {'name': 'arch2.jpeg', 'size': 128418, 'date': '2018-06-02 19:49:17.427922', 'restante': 1}
            ],
            'categoria2': [
                {'name': 'arch1.jpeg', 'size': 88418, 'date': '2018-05-14 19:49:17.427922', 'restante': 7},
                {'name': 'arch2.jpeg', 'size': 128418, 'date': '2018-06-22 19:49:17.427922', 'restante': 14},
                {'name': 'juef.zip', 'size': 9928418, 'date': '2018-06-20 19:49:17.427922', 'restante': 8},
                {'name': 'arc3.jpeg', 'size': 128418, 'date': '2018-06-02 19:49:17.427922', 'restante': 1}
            ],
            'Misc': [
                {'name': 'arch1.jpeg', 'size': 78498, 'date': '2018-05-94 03:04:17.427922', 'restante': 7},
                {'name': 'indice-231.jpg', 'size': 1128418, 'date': '2018-06-19 19:49:17.427922', 'restante': 5},
                {'name': 'pato-4-31.31.2018.zip', 'size': 1589142548, 'date': '2018-06-09 04:06:10.427922', 'restante': 3},
                {'name': 'document.pdf', 'size': 5781231, 'date': '2018-06-22 19:49:17.427922', 'restante': 12},
                {'name': 'NOTA.DSE', 'size': 884, 'date': '2018-06-15 19:19:17.427922', 'restante': 6}
            ]
        }
        ,
        'params': {}
    }
    return render_template("index.html", dv=dv)
