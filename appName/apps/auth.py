from functools import wraps
from ..functions import json_convert, cod_random, encript_passw
from flask import jsonify, request, abort, current_app

class Auth():

  def __init__(self, app):
      self.appVar = app
  # The actual decorator function
  def methods(self):
    app = self.appVar

    def require_appkey(view_function):
      @wraps(view_function)
      # the new, post-decoration function. Note *args and **kwargs here.
      def decorated_function(*args, **kwargs):
        with open(apiKey, 'r') as apikey:
          key = apikey.read().replace('\n', '')
        # if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
          return view_function(*args, **kwargs)
        else:
          abort(401)
      return decorated_function

    ## Registro de usuarios ##


    @app.route('/api/v0.1/register/', methods=['POST'])
    @require_appkey
    def register():
        externo = conexion.conexion_externa()
        try:
            externo_cursor = externo.cursor()
            new_user = {
                "tipo_doc": request.json['tipo_doc'],
                "documento": request.json['documento'],
                "nombre": request.json['nombre'],
                "username": request.json['username'],
                "correo": request.json['correo'],
                "password": request.json['password'],
                "telefono": request.json['telefono'],
                "rol": request.json['rol'],
                "ult_con": str(datetime.datetime.utcnow())
            }

            if not new_user['correo'] or not new_user['password'] or not new_user['nombre']:
                return jsonify({'result': "Not enough data"}), 406
            else:

                if "@" in new_user['correo']:
                    id_medica = cod_random(5)
                    # Validar correo:
                    externo_cursor.execute(
                        'SELECT * FROM tb_usuarios WHERE correo = "' + new_user['correo'] + '"')
                    datos = externo_cursor.fetchall()
                    indices = externo_cursor.description

                    result_email = json_convert(datos, indices)
                    if(result_email == []):
                        externo_cursor.execute(
                            'SELECT * FROM tb_usuarios WHERE documento = "' + new_user['documento'] + '"')
                        datos = externo_cursor.fetchall()
                        indices = externo_cursor.description

                        result_documento = json_convert(datos, indices)

                        if(result_documento == []):
                            # Validar username
                            externo_cursor.execute(
                                'SELECT * FROM tb_usuarios WHERE username = "' + new_user['username'] + '"')
                            datos = externo_cursor.fetchall()
                            indices = externo_cursor.description
                            result_username = json_convert(datos, indices)
                            if(result_username == []):

                                password = encript_passw(new_user['password'])

                                sql = 'INSERT INTO tb_usuarios (id_medica, tipo_doc, documento, nombre, username, correo, password, rol, telefono, ult_con) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                                val = (id_medica, new_user['tipo_doc'], new_user['documento'], new_user['nombre'], new_user['username'], new_user['correo'],
                                      password, new_user['rol'], new_user['telefono'], new_user['ult_con'])
                                externo_cursor.execute(sql, val)
                                externo.commit()

                                externo_cursor.execute(
                                    f'INSERT INTO tb_medica (id_medica) VALUES ("{id_medica}")')
                                externo.commit()

                                return jsonify({'result': 'Added successfully', 'id_medica': id_medica}), 201
                            else:
                                return jsonify({'result': "Username already registered"}), 406
                        else:
                            return jsonify({'result': "Document already registered"}), 406
                    else:
                        return jsonify({'result': "Email already registered"}), 406

                else:
                    return jsonify({'result': "Email verification error"}), 406
        except:
            return jsonify({'result': "Error adding user", 'error': sys.exc_info()[0]}), 405
        externo.close()

      ## Login de Usuarios ##

    @app.route('/api/v0.1/login/', methods=['POST'])
    @require_appkey
    def login():
      externo = conexion.conexion_externa()
      try:
        externo_cursor = externo.cursor()
        user = {
          "correo": request.json['correo'],
          "password": request.json['password'],
        }

        if not user['correo'] or not user['password']:
          return jsonify({'result': "Datos sin completar"}), 406
        else:
          externo_cursor.execute('SELECT documento, nombre, correo, username, password, rol FROM tb_usuarios WHERE documento="' + user['correo'] + '"')
          datos = externo_cursor.fetchall()
          indices = externo_cursor.description

          result = json_convert(datos, indices)
          if(result == []):
            externo.close()
            return jsonify({'result': 'Correo electrónico o código de empresa no válido'}), 405

          else:
            password_bd = result[0]['password']
            if(check_password_hash(password_bd, user['password'])):
              token = jwt.encode({
                'sub': user['correo'],
                'name': result[0]['nombre'],
                'username': result[0]['username'],
                'documento': str(result[0]['documento']),
                'rol': result[0]['rol'],
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + timedelta(minutes=400)},
                # 'exp': 1478773621},
                current_app.config['SECRET_KEY']
              )
              externo.close()
              return jsonify({'token': token.decode('UTF-8')}), 201
            else:
              externo.close()
              return jsonify({'result': 'Contraseña errónea'}), 405

      except:
        externo.close()
        return jsonify({'result': 'none', 'error': sys.exc_info()[0]}), 405

      