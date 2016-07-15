print ('runserver.py')

from botadero import app as application

application.debug = False # cuidado con esto a la hora de poner en produccion! (debe estar en False, True es para desarrollo)
#application.debug = True # cuidado con esto a la hora de poner en produccion! (debe estar en False, True es para desarrollo)

application.run(host='0.0.0.0')
