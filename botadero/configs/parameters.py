import os
import hashlib
from datetime import datetime as dt

class Parameters():
    totalStorage = 5000000000
    uploadDirectory = 'almacen'
    sizeLimitsAndTimeToDelete = [
        [{'500000': 15}],
        [{'1500000': 10}],
        [{'5000000': 5}],
    ]
    timeUnit = 'day'
    logLevel = 2
    digestCheck = True
    digestAlgorithm = 'sha1'
    digestAccelerated = False
    passwordUse = False
    captchaUse = False

    def create(self, app=None):
        if app is None:
            return
        self.totalStorage = app.config['TOTAL_STORAGE']
        self.uploadDirectory = app.config['UPLOAD_DIRECTORY']
        self.sizeLimitsAndTimeToDelete = app.config['SIZE_LIMITS_AND_TIME_TO_DELETE']
        #configFileName = ''
        self.timeUnit = app.config['TIME_UNIT']
        self.logLevel = app.config['LOG_LEVEL']
        self.digestCheck = app.config['DIGEST_CHECK']
        self.digestAlgorithm = app.config['DIGEST_ALGORITHM']
        self.digestAccelerated = app.config['DIGEST_ACCELERATED']
        self.passwordUse = app.config['PASSWORD_USE']
        self.captchaUse = app.config['CAPTCHA_USE']
    
    def __init__(self,app=None):
        self.create(app)
        
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
            '\ncaptchaUse: '+str(self.captchaUse)

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
            '\ncaptchaUse: '+str(self.captchaUse)
