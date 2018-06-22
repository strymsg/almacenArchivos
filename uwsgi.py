import os
from botadero import create_app
#from flaskbb.utils.helpers import ReverseProxyPathFix

import logging

_basepath = os.path.dirname(os.path.abspath(__file__))

# will throw an error if the config doesn't exist
#flaskbb = create_app(config='flaskbb.cfg')

#  Uncomment to use the middleware
#flaskbb.wsgi_app = ReverseProxyPathFix(flaskbb.wsgi_app)

app = Flask(config='botadero/configs/configs.py')

