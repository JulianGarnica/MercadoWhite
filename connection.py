import sys
import sqlalchemy
from ntpath import join
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL, MySQLdb
from appPool.functions import json_convert


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

    def create_databases(self, basedir, id_empresa, externo_bd):
        self.createConnection()
        local_bd = f'{self.BD_NAME}_{id_empresa}'
        # mysql://user:password@server
        engine = sqlalchemy.create_engine(
            f'mysql://{self.USERNAME}:{self.PASSWORD}@{self.HOST}')  # connect to server
        engine.execute(
            f"CREATE DATABASE IF NOT EXISTS {local_bd} CHARACTER SET utf8 COLLATE utf8_general_ci")  # create db
        engine.execute(f"USE {local_bd} ")  # select new db

        confirmar = False
        # Verificar si existen las mismas columnas

        for h in range(0, 2):

            # Cursor local y externo
            local_cursor = engine

            # Nombres de tablas locales
            # Sacar nombres a tablas locales
            sql = local_cursor.execute(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '{local_bd}'")
            tupla_nombres_local = sql.fetchall()  # Agregar a array
            nombres_tablas_Local = []
            for name in tupla_nombres_local:
                nombres_tablas_Local.append(name[0])

            # Nombres de tablas externas
            # Sacar nombres a tablas locales
            self.cursor.execute(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '{externo_bd}'")
            tupla_nombres_externa = self.cursor.fetchall()  # Agregar a array
            nombres_tablas_Externa = []
            for name in tupla_nombres_externa:
                nombres_tablas_Externa.append(name[0])

            # Contar tablas externas
            cant_tablas = len(nombres_tablas_Externa)
            # Bucle que se repite dependiendo de la cantidad de tablas
            for i in range(1, cant_tablas+1):
                columnas_Externa = []
                columnas_Local = []

                n_i = i-1
                nombre_i = nombres_tablas_Externa[n_i]

                # Si no existe la tabla en la base de datos local
                if nombre_i not in nombres_tablas_Local:

                    # Muestra el código de creación de la tabla externa
                    self.cursor.execute(f"SHOW CREATE TABLE {nombre_i}")
                    tupla_create_table = self.cursor.fetchall()
                    # Extraigo únicamente el código de creación
                    for createtable in tupla_create_table:
                        instru_MySql = createtable[1]

                    # Ejecuto el código de creación anteriormente extraído
                    local_cursor.execute(instru_MySql)

                else:
                    # Si la tabla existe hacer:

                    # Mostrar cantidad de columnas existentes en bd EXTERNA y en tabla actual
                    self.cursor.execute(
                        f"SHOW COLUMNS FROM {nombre_i} FROM {externo_bd}")
                    tupla_ShowColumns_table_Externa = self.cursor.fetchall()
                    for ShowColumns_Externa in tupla_ShowColumns_table_Externa:
                        columnas_Externa.append(ShowColumns_Externa[0])

                    # columnas_Externa almacenará los nombres de cada columna

                    contador_Col_Externa = len(columnas_Externa)

                    # Mostrar cantidad de columnas existentes en bd LOCAL y en tabla actual
                    sql = local_cursor.execute(
                        f"SHOW COLUMNS FROM {nombre_i} FROM {local_bd}")
                    tupla_ShowColumns_table_Local = sql.fetchall()
                    for ShowColumns_Local in tupla_ShowColumns_table_Local:
                        columnas_Local.append(ShowColumns_Local[0])

                    # Validante de Columnas
                    for g in range(0, contador_Col_Externa):
                        nombre_Externa = columnas_Externa[g]

                        if nombre_Externa not in columnas_Local:

                            self.cursor.execute(
                                f"SHOW COLUMNS FROM {nombre_i} IN {externo_bd} WHERE field = '{nombre_Externa}'")
                            query_crear_columna_TUPLA = self.cursor.fetchall()
                            """
                                ORDEN DE CREACIÓN DE TABLA:
                                NAME | TYPE | NULL | KEY | DEFAULT | EXTRA
                            """
                            for value in query_crear_columna_TUPLA:
                                name_var = (value[0])
                                type_var = (value[1])
                                null_var = (value[2])

                            if null_var == "YES":
                                null_var = "NULL"
                            else:
                                null_var = "NOT NULL"

                            add_query = f"{name_var} {type_var} {null_var}"

                            local_cursor.execute(
                                f"ALTER TABLE {nombre_i} ADD {add_query}")
        confirmar = True
        self.closeConnection()
        return confirmar

__all__ = ['externo_host', 'externo_user',
           'externo_password', 'externo_bd', 'externo_port']
