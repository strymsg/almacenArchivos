'''
Botadero, una aplicacion para compartir archivos libremente.
Copyright (C) 2016 Rodrigo Garcia <strysg@riseup.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
# cargar configuraciones del servidor
from flask import Flask

app = Flask(__name__, static_url_path='/static')

import botadero.views
import botadero.utils

app.config['UPLOAD_FOLDER'] = utils.ParametrosServer.UploadFolder

# blueprints
from botadero.archivos.views import mod as modulo_archivos
app.register_blueprint(modulo_archivos)

# ############## principal ########################
if __name__ == '__main__':
    print "running from main"
    print 
    print "------"

    app.run(host='0.0.0.0')

    # cargar configuraciones del servidor
    utils.EstadisticaArchivos.Inicializar()
    
    print "[PARAMETERS] - TOTAL_STORAGE=%d" %ParametrosServer.TotalStorage
    print "[PARAMETERS] - UPLOAD_FOLDER=%s" %ParametrosServer.UploadFolder
    print "[PARAMETERS] - SIZE_1=%d" %ParametrosServer.Size1
    print "[PARAMETERS] - SIZE_2=%d" %ParametrosServer.Size2
    print "[PARAMETERS] - TIME_TO_DEL_0=%d" %ParametrosServer.TimeToDel0
    print "[PARAMETERS] - TIME_TO_DEL_1=%d" %ParametrosServer.TimeToDel1
    print "[PARAMETERS] - TIME_TO_DEL_2=%d" %ParametrosServer.TimeToDel2
    print "[PARAMETERS] - SIZE_MAX_TO_UPLOAD=%d" %ParametrosServer.SizeMaxToUpload
    print "[PARAMETERS] - Log File =%s" %ParametrosServer.LogFileName
    print "[PARAMETERS] - Debug Level =%d" %ParametrosServer.DebugLevel

