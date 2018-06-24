import os
import hashlib
from datetime import datetime as dt

from flask import current_app as app

class Parameters():
    totalStorage = app.config['TOTAL_STORAGE']
    uploadDirectory = app.config['UPLOAD_DIRECTORY']
    sizeLimitsAndTimeToDelete = app.config['SIZE_LIMITS_AND_TIME_TO_DELETE']
    timeUnit = app.config['TIME_UNIT']
    logLevel = app.config['LOG_LEVEL']
    digestCheck = app.config['DIGEST_CHECK']
    digestAlgorithm = app.config['DIGEST_ALGORITHM']
    digestAccelerated = app.config['DIGEST_ACCELERATED']
    passwordUse = app.config['PASSWORD_USE']
    captchaUse = app.config['CAPTCHA_USE']

    def __init__(self,app=None):
        totalStorage = app.config['TOTAL_STORAGE']
        uploadDirectory = app.config['UPLOAD_DIRECTORY']
        sizeLimitsAndTimeToDelete = app.config['SIZE_LIMITS_AND_TIME_TO_DELETE']
        #configFileName = ''
        timeUnit = app.config['TIME_UNIT']
        logLevel = app.config['LOG_LEVEL']
        digestCheck = app.config['DIGEST_CHECK']
        digestAlgorithm = app.config['DIGEST_ALGORITHM']
        digestAccelerated = app.config['DIGEST_ACCELERATED']
        passwordUse = app.config['PASSWORD_USE']
        captchaUse = app.config['CAPTCHA_USE']

    def __str__(self):
        return '** Parameters **'+ \
            '\ntotalStorage:',str(self.totalStorage) + \
            '\nuploadDirectory:',self.uploadDirectory + \
            '\nsizeLimitsAndTimeToDelete:',str(self.sizeLimitsAndTimeToDelete) +\
            '\ntimeUnit:',self.timeUnit + \
            '\nlogLevel:',str(self.logLevel) + \
            '\ndigestCheck:',str(self.digestCheck) + \
            '\ndigestAlgorithm:',self.digestAlgorithm + \
            '\npasswordUse:',str(self.passwordUse) + \
            '\ncaptchaUse:',str(self.captchaUse)
