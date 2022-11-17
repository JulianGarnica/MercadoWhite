import sys
import os
import jwt
import datetime

from datetime import date, timedelta
from functools import wraps
from ..functions import  cod_random, encript_passw
from werkzeug.security import check_password_hash
from flask import jsonify, request, abort, current_app

class Auth():

  def __init__(self, app, connection, apiKey):
      self.appVar = app
      self.connection = connection
      self.apiKey = apiKey
      
  # The actual decorator function
  def methods(self):
    app = self.appVar

    def require_appkey(view_function):
      @wraps(view_function)
      # the new, post-decoration function. Note *args and **kwargs here.
      def decorated_function(*args, **kwargs):
        with open(self.apiKey, 'r') as apikey:
          key = apikey.read().replace('\n', '')
        # if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
          return view_function(*args, **kwargs)
        else:
          abort(401)
      return decorated_function

    ## Registro de usuarios ##


    @app.route('/auth/v0.1/register/', methods=['POST'])
    @require_appkey
    def register():
        try:
            try:
                new_user = {
                    "nombre": request.json['nombre'],
                    "correo": request.json['correo'],
                    "contrasena": str(request.json['contrasena']),
                    "fechaNacimiento": str(request.json['fechaNacimiento']),
                }
            except:
              return jsonify({'result': "Invalid data"}), 406

            if not new_user['correo'] or not new_user['contrasena'] or not new_user['nombre']:
                return jsonify({'result': "Not enough data"}), 406
            else:

                if "@" in new_user['correo']:
                    # Validar correo:
                    result_email = self.connection.query('SELECT * FROM tb_usuarios WHERE correo = "' + new_user['correo'] + '"')
                                      
                    if(result_email == []):

                          password = encript_passw(new_user['contrasena'])
                          print(password)
                          
                          self.connection.agregarUsuario(new_user["nombre"],new_user["correo"], password, new_user["fechaNacimiento"])

                          # basedir = str(app.config['UPLOAD_FOLDER'])+str('/clients/')+str(id_empresa)
                          # if(os.path.isdir(basedir)):
                          #     pass
                          # else: os.mkdir(basedir)
                          """
                          
                          columns = ("id_empresa")
                          val = (id_empresa)
                          self.connection.insert("tb_empresas", columns, val)

                          """
                          return jsonify({'result': 'Added successfully'}), 201
                        
                    else:
                        return jsonify({'result': "Email already registered"}), 406

                else:
                    return jsonify({'result': "Email verification error"}), 406
        except:
            return jsonify({'result': "Error adding user", 'error': str(sys.exc_info()[1])}), 405
        externo.close()

      ## Login de Usuarios ##

    @app.route('/auth/v0.1/login/', methods=['POST'])
    @require_appkey
    def login():
      try:
        user = {
          "correo": request.json['correo'],
          "contrasena": request.json['contrasena'],
        }

        if not user['correo'] or not user['contrasena']:
          return jsonify({'result': "Datos sin completar"}), 406
        else:

          result =self.connection.query('SELECT correo, contrasena FROM tb_usuarios WHERE correo="' + user['correo'] + '"')
          if(result == []):
            return jsonify({'result': 'Correo electrónico o código de empresa no válido'}), 405

          else:
            password_bd = result[0]['contrasena']
            if(check_password_hash(password_bd, user['contrasena'])):
              token = jwt.encode({
                'sub': "1",
                'email': result[0]['correo'],
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + timedelta(minutes=400)},
                # 'exp': 1478773621},
                current_app.config['SECRET_KEY']
              )
              return jsonify({'token': token}), 201
            else:
              return jsonify({'result': 'Contraseña errónea'}), 405

      except:
        return jsonify({'result': 'none', 'error': sys.exc_info()[0]}), 405
      
    @app.route('/auth/v0.1/updateUser/', methods=['POST'])
    @require_appkey
    def updateUser():
      id_empresa = request.json['id_empresa']
      basedir = str(app.config['UPLOAD_FOLDER'])+str('/clients/')+str(id_empresa)
      if(os.path.isdir(basedir)):
          pass
      else: os.mkdir(basedir)
      response = self.connectionDBgtPool.create_databases(basedir, id_empresa, "bd_gtpool")
      return jsonify({'result': response})
      