import sys
import os
import jwt
import datetime

from datetime import date, timedelta
from functools import wraps
from ..functions import  cod_random, encript_passw, allowed_file
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify, request, abort, current_app

class Productos():

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
    
    @app.route('/productos/v0.1/producto/', methods=['POST'])
    @require_appkey
    def agregarProducto():
      try:
        try:
          bodyRequest = {
              "categoria": request.form['categoria'],
              "valor": request.form['valor'],
              "nombre": request.form['nombre'],
              "stock": request.form['stock'],
          }
        except:
          print(sys.exc_info())
          return jsonify({'result': "Invalid data"}), 406
        
        # check if the post request has the file part
        if 'file' not in request.files:
          return jsonify({"result": "No file part"}), 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
          return jsonify({"result": "No selected file"}), 400
        if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          
          columns = ["Categoria", "Valor", "Nombre", "Images", "Stock"]
          values = [bodyRequest["categoria"], bodyRequest["valor"], bodyRequest["nombre"], filename, bodyRequest["stock"]]
          self.connection.insert("tb_productos", columns, values)
          
          return jsonify({"result": "New product uploaded successfully"})
        else:
          return jsonify({'result': "Image type invalid"}), 406
      except:
        return jsonify({'result': "Error adding product", 'error': str(sys.exc_info()[1])}), 405
        
        
    @app.route('/productos/v0.1/productos/', methods=['GET'])
    @require_appkey
    def consultarProductos():
      try:
        result_productos = self.connection.query('SELECT * FROM tb_productos')
        return jsonify({"result": result_productos})
      except:
        return jsonify({'result': "Error adding user", 'error': str(sys.exc_info()[1])}), 405
    
    @app.route('/productos/v0.1/producto/<idProd>', methods=['GET'])
    @require_appkey
    def consultarProductoPorId(idProd):
      try:
        result_productos = self.connection.query('SELECT * FROM tb_productos WHERE IdProducto="'+idProd+'"')
        return jsonify({"result": result_productos[0]})
      except:
        return jsonify({'result': "Producto no encontrado"}), 405
    
    @app.route('/productos/v0.1/productos/<category>', methods=['GET'])
    @require_appkey
    def consultarProductosConCategoria(category):
      try:
        result_productos = self.connection.query('SELECT * FROM tb_productos WHERE Categoria="'+category+'"')
        return jsonify({"result": result_productos})
      except:
        return jsonify({'result': "Categoría no encontrada"}), 405
      
    @app.route('/productos/v0.1/categorias/', methods=['GET'])
    @require_appkey
    def consultarCategorias():
      try:
        result_productos = self.connection.query('SELECT DISTINCT Categoria FROM tb_productos')
        return jsonify({"result": result_productos})
      except:
        return jsonify({'result': "Error consultando categorías", 'error': str(sys.exc_info()[1])}), 405