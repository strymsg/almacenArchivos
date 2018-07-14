'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <strysg@riseup.net>
AGPL liberated.
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime as dt

#from .database import CRUDMixin
#from .database import db
#db = SQLAlchemy()
from . import get_db
from . import CRUDMixin
from botadero.shared import globalParams

print ('modelos antes de get_db')
db = get_db()
print ('modelos (db)', str(db))

class Archivo(db.Model, CRUDMixin):
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

    def __init__(self, **kwargs):
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
        self.path = kwargs.get('path', globalParams.uploadDirectory)
        self.size = kwargs.get('size',0)
        self.extension = kwargs.get('extension','')
        self.downloads = kwargs.get('downloads', 0)
        self.digestCheck = kwargs.get('digetsCheck', '')
        self.digestAlgorithm = kwargs.get('digestAlgorithm',
                                          globalParams.digestAlgorithm)
        self.uploadedAtTime = kwargs.get('uploadedAtTime', str(dt.now()))
        self.remainingTime = kwargs.get('ramainingTime', 1)
        self.hashedPassword = kwargs.get('hashedPassword', '')

    def save(self, **kwargs):
        self.name = kwargs.get('name',self.name)
        self.path = kwargs.get('path', self.path)
        self.size = kwargs.get('size', self.size)
        self.extension = kwargs.get('extension', self.extension)
        self.downloads = kwargs.get('downloads', self.downloads)
        self.digestCheck = kwargs.get('digetsCheck', self.digestCheck)
        self.digestAlgorithm = kwargs.get('digestAlgorithm',
                                          self.digestAlgorithm)
        self.uploadedAtTime = kwargs.get('uploadedAtTime',
                                         self.uploadedAtTime)
        self.remainingTime = kwargs.get('ramainingTime',
                                        self.remainingTime)
        self.hashedPassword = kwargs.get('hashedPassword',
                                         self.hashedPassword)
        
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        return db.session.delete(self)
        #pass
        
    # def __repr__(self):
    #     return 'File %r/%r: [%r] (%r B), downloads: %d - uploaded: %r remaining time: %d' % (self.path, self.name, self.digestCheck, self.size, self.downloads, self.uploadedAtTime, self.remainingTime)
