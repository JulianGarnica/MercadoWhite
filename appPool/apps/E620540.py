import os
import inspect
import sys
from ..functions import  cod_random
from flask import jsonify, request

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir =  os.path.dirname(parentdir)
sys.path.insert(0, parentparentdir) 
import connection

##Class to add a new pool table

class E620540():
  
  def __init__(self, app, connection, apiKey):
    self.appVar = app
    self.connection = connection
    self.apiKey = apiKey
  # The actual decorator function
  def methods(self):
    app = self.appVar
    @app.route(f'{app.config["SLUG"]}updateTables/mesas_activas', methods=['POST'])
    def updateTables_mesas_activas():
      tempoPacho = request.json['VFPData']["tempopacho"]
      id_empresa = request.json["id_empresa"]
      
      bd_empresa = f"bd_gtpool_{id_empresa}"
      
      connection_bd_gtpool = connection.conn(app.config, bd_empresa)
      connection_bd_gtpool.truncateTable("tb_mesas_activas")
      for objectTempo in tempoPacho:
        columns = ("idPartida","doc_no", "fecha_hora", "id_equipo", "mesa", "porc_iva", "razon_soc", "vr_minuto")
        val = (cod_random(7), objectTempo["doc_no"], objectTempo["fecha_hora"], objectTempo["id_equipo"], objectTempo["mesa"], objectTempo["porc_iva"], objectTempo["razon_soc"], objectTempo["vr_minuto"])
        connection_bd_gtpool.insert("tb_mesas_activas", columns, val)
      
      result =connection_bd_gtpool.query('SELECT idPartida FROM tb_mesas_activas')
      return jsonify({'result': result}), 201
    
    @app.route(f'{app.config["SLUG"]}get/mesas_activas/<path:idEmpresa>/<path:idPartida>', methods=['GET'])
    def get_mesasActivas(idEmpresa, idPartida):
      bd_empresa = f"bd_gtpool_{idEmpresa}"
      connection_bd_gtpool = connection.conn(app.config, bd_empresa)
      result = connection_bd_gtpool.query('SELECT * FROM tb_mesas_activas WHERE idPartida = "' + idPartida + '"')
      return jsonify({'result': result}), 200