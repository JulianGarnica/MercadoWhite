import os
import inspect
import sys

from ..functions import cod_random
from flask import jsonify, request

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir =  os.path.dirname(parentdir)
sys.path.insert(0, parentparentdir) 
import connection
# Class to add a new pool table


class D620541():

    def __init__(self, app, connection, apiKey):
        self.appVar = app
        self.connection = connection
        self.apiKey = apiKey
    # The actual decorator function

    def methods(self):
        app = self.appVar

        @app.route(f'{app.config["SLUG"]}updateTables/productos_pedidos', methods=['POST'])
        def updateTables_productos_pedidos():
            tempoPacho = request.json['VFPData']["tempopacho"]
            id_empresa = request.json["id_empresa"]
            
            bd_empresa = f"bd_gtpool_{id_empresa}"
      
            connection_bd_gtpool = connection.conn(app.config, bd_empresa)

            connection_bd_gtpool.truncateTable("tb_productos_pedidos")
            for objectTempo in tempoPacho:
                columns = ("doc_no", "cod_prod", "cantidad", "vr_iva", "vr_total", "descuento",
                           "cortesia", "tipo", "fecha_hora", "comandita", "pedido_por", "control", "tmp01")
                val = (objectTempo["doc_no"], objectTempo["cod_prod"], objectTempo["cantidad"], objectTempo["vr_iva"], objectTempo["vr_total"], objectTempo["descuento"],
                       objectTempo["cortesia"], objectTempo["tipo"], objectTempo["fecha_hora"], objectTempo["comandita"], objectTempo["pedido_por"], objectTempo["control"], objectTempo["tmp01"])
                connection_bd_gtpool.insert("tb_productos_pedidos", columns, val)

            result = connection_bd_gtpool.query(
                'SELECT id FROM tb_productos_pedidos')
            return jsonify({'result': result}), 201

        @app.route(f'{app.config["SLUG"]}get/productos_pedidos/<path:idEmpresa>/<path:idPartida>', methods=['GET'])
        def get_productosPedidos(idEmpresa, idPartida):
          bd_empresa = f"bd_gtpool_{idEmpresa}"
          connection_bd_gtpool = connection.conn(app.config, bd_empresa)
          result = connection_bd_gtpool.query('SELECT * FROM tb_productos_pedidos WHERE pedido_por = "' + idPartida + '"')
          return jsonify({'result': result}), 200