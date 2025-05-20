# conectar_bd.py
import mysql.connector
from mysql.connector import Error

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',         # Reemplaza con tu host
            user='root',      # Reemplaza con tu usuario
            password='', # Reemplaza con tu contraseña
            database='centinela' # Reemplaza con tu base de datos
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return None
