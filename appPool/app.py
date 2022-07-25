import inspect
import json
import sys
import os
import ssl

from distutils.command.config import config
from .functions import *
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_cors import CORS
from .apps import *

#Imports from parent folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import connection



app = Flask(__name__,
            static_folder='./dist/static',
            template_folder='./dist/',
            )

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

###Make BD Connection###
connection_bd_gtpool = connection.conn(app.config, "bd_gtpool")
connection_ppscolombia = connection.conn(app.config, "bd_ppscolombia")


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'upload')
app.config['UPLOAD_FOLDER'] =os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + app.config['IMAGE_UPLOADS']
app.config['SECRET_KEY'] = app.config['SECRET_KEY']
app.config['SLUG'] = "/appPool/"

cors = CORS(app, resources={r"/auth/*": {"origins": "*"}})
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

# apiKey = "./cert/api.key"
# sslCert = './cert/ssl.cert'
# sslKey = './cert/ssl.key'
apiKey = "./cert/api.key"
sslCert = './cert/ssl.cert'
sslKey = './cert/ssl.key'
context.load_cert_chain(sslCert, sslKey)


if app.config["HAS_FRONT_AUTHAPP"]:
    @app.route('/', defaults={'path': '/'})
    @app.route('/<path:path>')
    def render_vue(path):
        print("Está válido")
        return render_template('index.html')



###Apps###
app_E620540 = E620540(app, connection_bd_gtpool, apiKey)
app_E620540.methods()

app_auth = Auth(app, connection_ppscolombia, connection_bd_gtpool, apiKey)
app_auth.methods()


__all__ = ['app']