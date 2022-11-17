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

class Pedidos():

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
    
    @app.route('/pedidos/v0.1/pedido/', methods=['POST'])
    @require_appkey
    def agregarPedido():
      try:
        try:
          bodyRequest = {
              "IdCliente": request.json['IdCliente'],
              "TipoDePago": request.json['TipoDePago'],
              "PrecioTotal": request.json['PrecioTotal'],
              "productos": request.json['productos'],
              "Direccion": request.json['Direccion'],
              "NombreQuienRecibe": request.json['NombreQuienRecibe'],
              "Telefono": request.json["Telefono"],
              "ValorEnvio": request.json["ValorEnvio"]
          }
        except:
          print(sys.exc_info())
          return jsonify({'result': "Invalid data"}), 406

        fecha = datetime.date.today()

        columns = ["Direccion", "NombreQuienRecibe", "Telefono", "ValorEnvio"]
        values = [bodyRequest["Direccion"], bodyRequest["NombreQuienRecibe"], bodyRequest["Telefono"], bodyRequest["ValorEnvio"]]
        self.connection.insert("tb_envios", columns, values)
        idEnvios = self.connection.returnLastID("tb_envios", "IdEnvio")[0]["IdEnvio"]
        
        columns = ["Fecha", "IdClienteRel", "IdEnvioRel", "TipoDePago", "PrecioTotal"]
        values = [fecha, bodyRequest["IdCliente"], idEnvios, bodyRequest["TipoDePago"], bodyRequest["PrecioTotal"]]
        self.connection.insert("tb_ventas", columns, values)
        idVenta = self.connection.returnLastID("tb_ventas", "IdVenta")[0]["IdVenta"]
        
        for producto in bodyRequest["productos"]:
          columns = ["IdVentaRel", "IdProductoRel", "Cantidad", "PrecioUnitario"]
          values = [idVenta, producto["id"], producto["Cantidad"], producto["PrecioUnitario"]]
          self.connection.insert("tb_productosSeleccionados", columns, values)
          
        return jsonify({"result": "New order created successfully"})
      except:
        return jsonify({'result': "Error adding order", 'error': str(sys.exc_info()[1])}), 405
    
    @app.route('/pedidos/v0.1/pedido/<idPedido>', methods=['get'])
    @require_appkey
    def consultarPedido(idPedido):
      try:
        result = {}
        result_ventas = self.connection.query('SELECT tv.Fecha, tv.TipoDePago, tv.PrecioTotal, tu.Nombre, tu.Correo, te.Direccion, te.NombreQuienRecibe, te.Telefono, te.ValorEnvio FROM tb_ventas tv INNER JOIN tb_usuarios tu ON tv.IdClienteRel = tu.Id INNER JOIN tb_envios te ON tv.IdEnvioRel = te.IdEnvio WHERE IdVenta="'+idPedido+'"')
        result = result_ventas[0]
        result["productos"] = self.connection.query('SELECT tps.Cantidad, tps.PrecioUnitario, tprod.Categoria, tprod.Nombre FROM tb_productosSeleccionados tps INNER JOIN tb_productos tprod on tps.IdProductoRel = tprod.IdProducto WHERE idVentaRel="'+idPedido+'"')
        
        return jsonify({"result": result})
      except:
        print(sys.exc_info())
        return jsonify({'result': "Pedido no encontrado"}), 405