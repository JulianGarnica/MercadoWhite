import inspect
import json
import sys
import os
import ssl

from distutils.command.config import config

from .functions import *
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_from_directory, jsonify
from threading import Lock
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
    print("Production")
    app.config.from_object("config.ProductionConfig")
else:
    print("Dev")
    app.config.from_object("config.DevelopmentConfig")


###Make BD Connection###
connection_bd = connection.conn(app.config, "bd_MercadoWhite")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'upload')
app.config['UPLOAD_FOLDER'] =os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + app.config['IMAGE_UPLOADS']
app.config['SECRET_KEY'] = app.config['SECRET_KEY']
app.config['SLUG'] = "/appPool/"
async_mode = None
thread = None
thread_lock = Lock()

cors = CORS(app, resources={r"/*": {"origins": "*"}})
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

app_auth = Auth(app, connection_bd, apiKey)
app_auth.methods()

app_Productos = Productos(app, connection_bd, apiKey)
app_Productos.methods()

app_Pedidos = Pedidos(app, connection_bd, apiKey)
app_Pedidos.methods()


__all__ = ['app','socketio']