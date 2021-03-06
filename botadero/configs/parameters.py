import os
import hashlib
from datetime import datetime as dt

class Parameters():
    totalStorage = 5000000000
    uploadDirectory = 'almacen'
    sizeLimitsAndTimeToDelete = [
        ('500000', 15),
        ('1500000', 10),
        ('5000000', 5),
    ]
    timeUnit = 'day'
    logLevel = 2
    digestCheck = True
    digestAlgorithm = 'sha1'
    digestAccelerated = False
    passwordUse = False
    captchaUse = False
    applicationTitle = 'Almacén público de archivos'
    cssSchemes = ('gris1', 'verde1','azul1','amarillo1', 'rojo1','cafe1')

    def ordenar_limites(self, lista):
        tamanyos = sorted([tupla[0] for tupla in lista], reverse=True)
        # print(lista)
        # print('-------------')
        # print(tamanyos)
        ordenado = []
        for tam in tamanyos:
            found = False
            j = 0
            while not found and j < len(tamanyos):
                if lista[j][0] == tam:
                    found = True
                    ordenado.append((tam, lista[j][1]))
                j = j + 1
        return ordenado
        
    def create(self, app=None):
        if app is None:
            return
        self.totalStorage = app.config['TOTAL_STORAGE']
        self.uploadDirectory = app.config['UPLOAD_DIRECTORY']
        self.sizeLimitsAndTimeToDelete = self.ordenar_limites(
            app.config['SIZE_LIMITS_AND_TIME_TO_DELETE'])
        #l = app.config['SIZE_LIMITS_AND_TIME_TO_DELETE']
        # self.sizeLimitsAndTimeToDelete = sorted(l,
        #                                         key=lambda l: l[0],
        #                                         reverse=True)
        self.timeUnit = app.config['TIME_UNIT']
        self.logLevel = app.config['LOG_LEVEL']
        self.digestCheck = app.config['DIGEST_CHECK']
        self.digestAlgorithm = app.config['DIGEST_ALGORITHM']
        self.digestAccelerated = app.config['DIGEST_ACCELERATED']
        self.passwordUse = app.config['PASSWORD_USE']
        self.captchaUse = app.config['CAPTCHA_USE']
        self.applicationTitle = app.config['APPLICATION_TITLE']
        self.cssSchemes = app.config['CSS_SCHEMES']
        
    def __init__(self, app=None):
        self.create(app=app)
        
    def __str__(self):
        return '** Parameters **'+ \
            '\ntotalStorage: '+str(self.totalStorage) + \
            '\nuploadDirectory: '+self.uploadDirectory + \
            '\nsizeLimitsAndTimeToDelete: '+str(self.sizeLimitsAndTimeToDelete) +\
            '\ntimeUnit: '+self.timeUnit + \
            '\nlogLevel: '+str(self.logLevel) + \
            '\ndigestCheck: '+str(self.digestCheck) + \
            '\ndigestAlgorithm: '+self.digestAlgorithm + \
            '\npasswordUse: '+str(self.passwordUse) + \
            '\ncaptchaUse: '+str(self.captchaUse) + \
            '\napplicationTitle: '+str(self.applicationTitle) + \
            '\ncssSchemes: '+str(self.cssSchemes)

    def __repr__(self):
        return '-- Parameters '+ \
            '\ntotalStorage: '+str(self.totalStorage) + \
            '\nuploadDirectory: '+self.uploadDirectory + \
            '\nsizeLimitsAndTimeToDelete: '+str(self.sizeLimitsAndTimeToDelete) +\
            '\ntimeUnit: '+self.timeUnit + \
            '\nlogLevel: '+str(self.logLevel) + \
            '\ndigestCheck: '+str(self.digestCheck) + \
            '\ndigestAlgorithm: '+self.digestAlgorithm + \
            '\npasswordUse: '+str(self.passwordUse) + \
            '\ncaptchaUse: '+str(self.captchaUse) + \
            '\napplicationTitle: '+str(self.applicationTitle) + \
            '\ncssSchemes: '+str(self.cssSchemes)
