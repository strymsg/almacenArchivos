from sqlalchemy import Column, Integer, String
from .database import Base
from datetime import datetime as dt


# import configs and defaults
# ...

class Parametros(Base):
    __tablename__ = 'parametros'
    id = Column(Integer, primary_key=True)
    name = Column(String(1000), nullable=False)
    path = Column(String(1000), nullable=False)
    size = Column(Integer, default=0)
    extension = Column(String(20), default='', nullable=False)
    downloads = Column(Integer, default=0)
    digestCheck = Column(String(1024), default='')
    digestAlgorithm = Column(String(100), default='')
    uploadedAtTime = Column(String(100), default='')
    remainingTime = Column(Integer, default=1)
    hashedPassword = Column(String(2048), default='')

    def __init__(self, **kwargs):
        ''' Inicializador de columna Parametros, puede recibir los argumentos:
        - name: string
        - path: string
        - size: int
        - extension: string
        - downloads: int
        - digestCheck: string
        - digestAlgorithm: string
        - uploadadedAtTime: string (format expected: YYYY-MM-DD hh:mm:ss.ss)
        - reaminingTime: int (time unit ramining time)
        - hashedPassword: string
        '''
        self.name = kwargs.get('name','undefined')
        self.path = kwargs.get('path','.') #default
        self.size = kwargs.get('size',0)
        self.extension = kwargs.get('extension','')
        self.downloads = kwargs.get('downloads', 0)
        self.digestCheck = kwargs.get('digetsCheck', '')
        self.digestAlgorithm = kwargs.get('digestAlgorithm','') # default
        self.uploadedAtTime = kwargs.get('uploadedAtTime', str(dt.now()))
        self.remainingTime = kwargs.get('ramainingTime', 1)
        self.hashedPassword = kwargs.get('hashedPassword', '')

    def __repr__(self):
        return 'File %r/%r: [%r] (%r B), downloads: %d - uploaded: %r remaining time: %d' % (self.path, self.name, self.digestCheck, self.size, self.downloads, self.uploadadedAtTime, self,remainingTime)

    
        
    
    
    
