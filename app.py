"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
#Importacion de librerias a usar
from flask import Flask, request, render_template, session, redirect, jsonify, g
import numpy as np
import pandas as pd
import sqlalchemy as db
import sqlite3
#Definicion de la app flask
app = Flask(__name__)
#Se define el inicio para la base de datos con la ruta
engine = db.create_engine('sqlite:///users.db')
#Se conecta
connection = engine.connect()
metadata = db.MetaData()
#Se "refleja" o copia los datos de la BD para poder usarlos
users = db.Table('users', metadata, autoload=True, autoload_with=engine)
#print(users.columns.keys())
#print(repr(metadata.tables['users']))
query = db.select([users])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
#print(ResultSet)
#Se definen los datos de la BD en pandas para mostrarlos de manera mas ordenada
df = pd.DataFrame(ResultSet)
df.columns = ResultSet[0].keys()
#print(df)
#df.to_html('pandas.html')
#print(df)
#Definicion de funcion para la ruta /users/list
@app.route('/users/list', methods=("POST", "GET"))
def html_table():

    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
#Definicion de las funciones para la ruta /api/v1/users/
@app.route('/api/v1/users/', methods=("POST", "GET"))
def get_json():
    #result = connection.execute(users)
    return jsonify(tables=[df.to_html(classes='data')])
#Definicion de la funcion principal y ejecucion de la aplicacion en flask
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
