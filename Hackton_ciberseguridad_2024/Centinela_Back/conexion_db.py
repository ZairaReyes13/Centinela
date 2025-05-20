# conexion_bd.py

import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Conexión a la base de datos MySQL
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='centinela'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
        return conexion
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None

# Función para guardar predicciones en la tabla Prediccion_Riesgo
# Modificar la función para guardar predicciones
def guardar_predicciones(predicciones, zonas_riesgo, probabilidad_incidente, tipo_prediccion):
    conexion = conectar_bd()
    if conexion is None:
        print("Error: No se pudo establecer la conexión a la base de datos.")
        return
    
    cursor = conexion.cursor()

    try:
        for i in range(len(predicciones)):
            id_zona_riesgo = int(zonas_riesgo[i])  # Convertir a int
            probabilidad = float(probabilidad_incidente[i])  # Convertir a float
            tipo = tipo_prediccion[i]
            descripcion = f"Predicción generada para la zona de riesgo {id_zona_riesgo}"
            fecha_prediccion = datetime.now()

            consulta_insert = """
            INSERT INTO Prediccion_Riesgo (id_zona_riesgo, probabilidad_incidente, tipo_prediccion, fecha_prediccion, descripcion_prediccion)
            VALUES (%s, %s, %s, %s, %s)
            """
            valores = (id_zona_riesgo, probabilidad, tipo, fecha_prediccion, descripcion)

            # Validar los valores que se van a insertar
            print(f"Insertando en Prediccion_Riesgo: {valores}")

            cursor.execute(consulta_insert, valores)

        conexion.commit()
        print("Predicciones guardadas exitosamente en la base de datos.")
        
    except Error as e:
        print(f"Error al guardar predicciones: {e}")
        conexion.rollback()  # Deshacer cambios si hay un error
    finally:
        cursor.close()
        conexion.close()
