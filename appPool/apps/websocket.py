import sys
import os
import jwt
import datetime

from datetime import date, timedelta
from functools import wraps
from ..functions import  cod_random, encript_passw
from werkzeug.security import check_password_hash
from flask import jsonify, request, abort, current_app, session
from flask_socketio import emit, disconnect, send

class WebSocket():

  def __init__(self, app, connection, connectiongtPool, apiKey):
      self.appVar = app
      self.connection = connection
      self.connectionDBgtPool = connectiongtPool
      self.apiKey = apiKey
      
  # The actual decorator function
  def methods(self):
    socketio = self.appVar
    
    @socketio.on('message')
    def handleMessage(msg):
      print('message: '+msg)
      send(msg)
    
    @socketio.on('getEvent')
    def test_message(message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
            {'data': message['data'], 'count': session['receive_count']})
        
    @socketio.on('getPuntajes')
    def getPuntajes(message):
      print(message)
      emit( {'my_response', {'data': 'xd'}}, broadcast=True )