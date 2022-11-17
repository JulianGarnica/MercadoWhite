import sys
import sqlalchemy
from ntpath import join
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL, MySQLdb
from appMercadoWhite.functions import json_convert


class conn():

    def __init__(self, appConfig, bd):

        self.HOST = appConfig['DB_HOST']
        self.USERNAME = appConfig['DB_USERNAME']
        self.PASSWORD = appConfig['DB_PASSWORD']
        self.BD_NAME = bd
        self.PORT = appConfig['DB_PORT']

    def createConnection(self):
        self.conn = MySQLdb.connect(host=self.HOST,
                                    user=self.USERNAME,
                                    passwd=self.PASSWORD,
                                    db=self.BD_NAME,
                                    port=self.PORT)
        self.cursor = self.conn.cursor()
        print("Conexion hecha")

    def closeConnection(self):
        self.conn.close()

    def query(self, sql):
        self.createConnection()
        self.cursor.execute(sql)
        datos = self.cursor.fetchall()
        indices = self.cursor.description
        self.closeConnection()
        return json_convert(datos, indices)

    def insert(self, table, columns, values):
        try:
            self.createConnection()
            columnsString = ",".join(columns)
            percentSChar = ",".join(["%s" for x  in range(len(values))])
            sql = f'INSERT INTO {table} ({columnsString}) VALUES ({percentSChar})'
            self.cursor.execute(sql, values)
            self.conn.commit()
            self.closeConnection()
            return True
        except:
            print(sys.exc_info()[1])
            self.closeConnection()
            return False
        
    def returnLastID(self, table, idColumn):
        try:            
            self.createConnection()
            sql = f'SELECT {idColumn} FROM {table} ORDER BY {idColumn} DESC LIMIT 1'
            self.cursor.execute(sql)
            datos = self.cursor.fetchall()
            indices = self.cursor.description
            
            self.closeConnection()
            return json_convert(datos, indices)
        except:
            print(sys.exc_info()[1])
            self.closeConnection()
            return False
        
    def truncateTable(self, table):
        try:
            self.createConnection()
            sql = f'TRUNCATE TABLE {table}'
            self.cursor.execute(sql)
            self.conn.commit()
            self.closeConnection()
            return True
        except:
            print(sys.exc_info()[1])
            self.closeConnection()
            return False

    def agregarUsuario(self, nombre, correo, contrasena, fechaNacimiento):
        columns = ["Nombre", "Correo", "Contrasena", "FechaNacimiento"]
        values = [nombre, correo, contrasena, fechaNacimiento]
        self.insert("tb_usuarios", columns, values)
        
    
__all__ = ['externo_host', 'externo_user',
           'externo_password', 'externo_bd', 'externo_port']
