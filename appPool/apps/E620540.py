from multiprocessing import connection
from ..functions import  cod_random
from flask import jsonify, request, abort, current_app

##Class to add a new pool table

class E620540():
  
  def __init__(self, app, connection, apiKey):
    self.appVar = app
    self.connection = connection
    self.apiKey = apiKey
  # The actual decorator function
  def methods(self):
    app = self.appVar
    @app.route(f'{app.config["SLUG"]}updateTables/', methods=['POST'])
    def updateTables():
      tempoPacho = request.json['VFPData']["tempopacho"]
      
      self.connection.truncateTable("tb_mesas_activas")
      for objectTempo in tempoPacho:
        columns = ("idPartida","doc_no", "fecha_hora", "id_equipo", "mesa", "porc_iva", "razon_soc", "vr_minuto")
        val = (cod_random(7), objectTempo["doc_no"], objectTempo["fecha_hora"], objectTempo["id_equipo"], objectTempo["mesa"], objectTempo["porc_iva"], objectTempo["razon_soc"], objectTempo["vr_minuto"])
        self.connection.insert("tb_mesas_activas", columns, val)
      
      result =self.connection.query('SELECT idPartida FROM tb_mesas_activas')
      return jsonify({'result': result}), 201