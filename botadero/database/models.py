from sqlalchemy import Column, Integer, String
from .database import Base
from datetime import datetime as dt

from flask import current_app as app
from . import db

class Archivo(db.Model):
    __tablename__ = 'archivos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    path = db.Column(db.String(1000), nullable=False)
    size = db.Column(db.Integer, default=0)
    extension = db.Column(db.String(20), default='', nullable=False)
    downloads = db.Column(db.Integer, default=0)
    digestCheck = db.Column(db.String(1024), default='')
    digestAlgorithm = db.Column(db.String(100), default='')
    uploadedAtTime = db.Column(db.String(100), default='')
    remainingTime = db.Column(db.Integer, default=1)
    hashedPassword = db.Column(db.String(2048), default='')

    def __init__(**kwargs):
        super(Archivo, self).__init__(**kwargs)
        ''' Inicializador de columna Parametros, puede recibir los argumentos:
        - name: string
        - path: string
        - size: int
        - extension: string
        - downloads: int
        - digestCheck: string
        - digestAlgorithm: string
        - uploadadedAtTime: string (format expected: YYYY-MM-DD hh:mm:ss.ss)
        - reaminingTime: int (time unit remaining time)
        - hashedPassword: string
        '''
        self.name = kwargs.get('name','undefined')
        self.path = kwargs.get('path', app.config['UPLOAD_DIRECTORY'])
        self.size = kwargs.get('size',0)
        self.extension = kwargs.get('extension','')
        self.downloads = kwargs.get('downloads', 0)
        self.digestCheck = kwargs.get('digetsCheck', '')
        self.digestAlgorithm = kwargs.get('digestAlgorithm',
                                          app.config['DIGEST_ALGORITHM'])
        self.uploadedAtTime = kwargs.get('uploadedAtTime', str(dt.now()))
        self.remainingTime = kwargs.get('ramainingTime', 1)
        self.hashedPassword = kwargs.get('hashedPassword', '')

    def __repr__(self):
        return 'File %r/%r: [%r] (%r B), downloads: %d - uploaded: %r remaining time: %d' % (self.path, self.name, self.digestCheck, self.size, self.downloads, self.uploadadedAtTime, self,remainingTime)
