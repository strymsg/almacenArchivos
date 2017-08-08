print ('Ejecutando desde runserver.py')

from botadero import app as application

#application.debug = False # cuidado con esto a la hora de poner en produccion! (debe estar en False, True es para desarrollo)
application.debug = True # cuidado con esto a la hora de poner en produccion! (debe estar en False, True es para desarrollo)

from botadero import utils

# ############## principal ########################
if __name__ == '__main__':
    print "running from main"
    print "------"

    # cargar configuraciones del servidor
    utils.Ea.Inicializar()

    print("[PARAMETERS] - TOTAL_STORAGE=%d" %utils.ParametrosServer.TotalStorage)
    print("[PARAMETERS] - UPLOAD_FOLDER=%s" %utils.ParametrosServer.UploadFolder)
    print("[PARAMETERS] - SIZE_1=%d" %utils.ParametrosServer.Size1)
    print("[PARAMETERS] - SIZE_2=%d" %utils.ParametrosServer.Size2)
    print("[PARAMETERS] - TIME_TO_DEL_0=%d" %utils.ParametrosServer.TimeToDel0)
    print("[PARAMETERS] - TIME_TO_DEL_1=%d" %utils.ParametrosServer.TimeToDel1)
    print("[PARAMETERS] - TIME_TO_DEL_2=%d" %utils.ParametrosServer.TimeToDel2)
    print("[PARAMETERS] - SIZE_MAX_TO_UPLOAD=%d" %utils.ParametrosServer.SizeMaxToUpload)
    print("[PARAMETERS] - Log File =%s" %utils.ParametrosServer.LogFileName)
    print("[PARAMETERS] - Debug Level =%d" %utils.ParametrosServer.DebugLevel)
    print("[PARAMETERS] - HASH_ALGORITHM =%s" %utils.ParametrosServer.HashAlgorithm)
    print("[PARAMETERS] - ACCELERATE_HASH =%s" %utils.ParametrosServer.AccelerateHash)
    
    application.run(host='0.0.0.0')
