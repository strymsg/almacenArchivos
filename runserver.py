print ('runserver.py')

from botadero import app as application

application.debug = True # cuidado con esto a la hora de poner en produccion!

application.run(host='0.0.0.0')
